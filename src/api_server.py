#!/usr/bin/env python3
"""
Gemma 3 270M OpenAI-Compatible API Server (CPU-Only)

A lightweight API server providing OpenAI-compatible endpoints for the Gemma 3 270M model.
Optimized for CPU-only inference with minimal dependencies.

Endpoints:
    - /v1/chat/completions - Chat completions (OpenAI-compatible)
    - /v1/completions - Text completions
    - /v1/models - List available models
    - /health - Health check

Usage:
    python src/api_server.py
    docker run -p 8080:8080 gemma-3-270m-minimal python src/api_server.py
"""

import asyncio
import json
import platform
import time
import traceback
from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncGenerator, List, Dict, Any, Optional

import torch
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from transformers import AutoConfig, AutoModelForCausalLM, AutoTokenizer

# Model configuration
MODEL_PATH = "/app/data/model"
MODEL_NAME = "gemma-3-270m"

# Global model and tokenizer
model = None
tokenizer = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load model at startup."""
    global model, tokenizer
    
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, trust_remote_code=True)

    quantized = Path(MODEL_PATH) / "model_quantized.pt"
    if quantized.exists():
        print("Loading INT8-quantized model on CPU...")
        # Match the backend used at quantization build time: qnnpack on ARM64,
        # fbgemm (default) on x86.  The serialized packed weights are
        # backend-specific, so this must agree with quantize_model.py.
        arch = platform.machine().lower()
        if arch in ("arm64", "aarch64"):
            torch.backends.quantized.engine = "qnnpack"
        config = AutoConfig.from_pretrained(MODEL_PATH, trust_remote_code=True)
        model = AutoModelForCausalLM.from_config(config, trust_remote_code=True)
        # Apply the same quantize_dynamic transformation used at build time so
        # that the state-dict keys match before we load the weights.
        model = torch.quantization.quantize_dynamic(
            model, {torch.nn.Linear}, dtype=torch.qint8
        )
        # weights_only=False is required for quantized (qint8) tensor objects
        state_dict = torch.load(str(quantized), map_location="cpu", weights_only=False)
        model.load_state_dict(state_dict)
    else:
        print("Loading Gemma 3 270M model on CPU...")
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_PATH,
            torch_dtype=torch.bfloat16,
            device_map="cpu",
            low_cpu_mem_usage=True,
            trust_remote_code=True,
        )
    model.eval()

    try:
        print(f"✓ Model loaded! Memory: {model.get_memory_footprint() / 1024 / 1024:.0f} MB")
    except AttributeError:
        print("✓ Model loaded successfully!")
    yield


# FastAPI app
app = FastAPI(
    title="Gemma 3 270M API",
    description="OpenAI-compatible API for Gemma 3 270M LLM (CPU-only)",
    version="1.0.0",
    lifespan=lifespan
)


# Request models
class ChatMessage(BaseModel):
    role: str
    content: str


class ChatCompletionRequest(BaseModel):
    model: str = MODEL_NAME
    messages: List[ChatMessage]
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    max_completion_tokens: Optional[int] = None  # OpenAI SDK >=1.x alias
    top_p: float = 0.95
    top_k: int = 50
    stream: bool = False

    @property
    def effective_max_tokens(self) -> int:
        return self.max_completion_tokens or self.max_tokens or 256


class CompletionRequest(BaseModel):
    model: str = MODEL_NAME
    prompt: str
    temperature: float = 0.7
    max_tokens: int = 256
    top_p: float = 0.95
    top_k: int = 50
    stream: bool = False


# Response models
class Choice(BaseModel):
    index: int
    message: ChatMessage
    finish_reason: str


class CompletionChoice(BaseModel):
    index: int
    text: str
    finish_reason: str


class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ChatCompletionResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: List[Choice]
    usage: Usage


class CompletionResponse(BaseModel):
    id: str
    object: str = "text_completion"
    created: int
    model: str
    choices: List[CompletionChoice]
    usage: Usage


class ModelInfo(BaseModel):
    id: str
    object: str = "model"
    owned_by: str = "gemma-3-270m"
    created: int


def generate_response(
    prompt: str,
    max_tokens: int = 256,
    temperature: float = 0.7,
    top_p: float = 0.95,
    top_k: int = 50,
    do_sample: bool = False
) -> str:
    """Generate a response from the model."""

    # Tokenize input
    inputs = tokenizer(prompt, return_tensors="pt").to("cpu")
    input_length = inputs["input_ids"].shape[1]

    # temperature=0 means greedy decoding; do_sample requires temperature > 0
    use_sampling = temperature > 0.0 and temperature != 1.0
    gen_kwargs: dict = {
        "max_new_tokens": max_tokens,
        "do_sample": use_sampling,
        "pad_token_id": tokenizer.eos_token_id,
    }
    if use_sampling:
        gen_kwargs["temperature"] = temperature
        gen_kwargs["top_k"] = top_k
        gen_kwargs["top_p"] = top_p

    # Generate response
    try:
        with torch.no_grad():
            outputs = model.generate(**inputs, **gen_kwargs)
    except Exception:
        print("ERROR in model.generate():", flush=True)
        traceback.print_exc()
        raise

    # Decode response
    response = tokenizer.decode(
        outputs[0][input_length:],
        skip_special_tokens=True
    )

    return response.strip()


async def stream_response(
    prompt: str,
    max_tokens: int = 256,
    temperature: float = 0.7,
    top_p: float = 0.95,
    top_k: int = 50
) -> AsyncGenerator[str, None]:
    """Stream response token by token."""
    
    inputs = tokenizer(prompt, return_tensors="pt").to("cpu")
    input_length = inputs["input_ids"].shape[1]
    
    generated_tokens = 0
    do_sample = temperature != 1.0
    
    # Token-by-token generation
    with torch.no_grad():
        for _ in range(max_tokens):
            gen_kwargs = {
                "max_new_tokens": generated_tokens + 1,
                "do_sample": do_sample,
                "temperature": temperature,
                "top_k": top_k,
                "top_p": top_p,
                "pad_token_id": tokenizer.eos_token_id,
            }
            
            outputs = model.generate(**inputs, **gen_kwargs)
            current_text = tokenizer.decode(
                outputs[0][input_length:],
                skip_special_tokens=True
            )
            
            if generated_tokens > 0:
                delta = current_text[len(previous_text):]
            else:
                delta = current_text
            
            previous_text = current_text
            generated_tokens += 1
            
            # Send SSE event
            event = {
                "id": f"chatcmpl-{int(time.time())}",
                "object": "chat.completion.chunk",
                "created": int(time.time()),
                "model": MODEL_NAME,
                "choices": [
                    {
                        "index": 0,
                        "delta": {"content": delta},
                        "finish_reason": None
                    }
                ]
            }
            yield f"data: {json.dumps(event)}\n\n"
            
            # Check for stop token
            if tokenizer.eos_token in current_text:
                break
    
    # Send finish event
    finish_event = {
        "id": f"chatcmpl-{int(time.time())}",
        "object": "chat.completion.chunk",
        "created": int(time.time()),
        "model": MODEL_NAME,
        "choices": [
            {
                "index": 0,
                "delta": {},
                "finish_reason": "stop"
            }
        ]
    }
    yield f"data: {json.dumps(finish_event)}\n\n"
    yield "data: [DONE]\n\n"


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "model": MODEL_NAME}


@app.get("/v1/models")
async def list_models():
    """List available models."""
    return {
        "object": "list",
        "data": [
            ModelInfo(
                id=MODEL_NAME,
                created=int(time.time())
            )
        ]
    }


@app.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    """Handle chat completion requests."""
    
    # Format messages as prompt
    prompt = ""
    for msg in request.messages:
        if msg.role == "system":
            prompt += f"<bos><start_of_turn>system\n{msg.content}<end_of_turn>\n"
        elif msg.role == "user":
            prompt += f"<start_of_turn>user\n{msg.content}<end_of_turn>\n"
        elif msg.role == "assistant":
            prompt += f"<start_of_turn>model\n{msg.content}<end_of_turn>\n"
    prompt += "<start_of_turn>model\n"
    
    if request.stream:
        # Streaming response
        return StreamingResponse(
            stream_response(
                prompt,
                max_tokens=request.effective_max_tokens,
                temperature=request.temperature,
                top_p=request.top_p,
                top_k=request.top_k
            ),
            media_type="text/event-stream"
        )

    # Non-streaming response
    response_text = generate_response(
        prompt,
        max_tokens=request.effective_max_tokens,
        temperature=request.temperature,
        top_p=request.top_p,
        top_k=request.top_k
    )
    
    # Calculate token usage
    prompt_tokens = len(tokenizer.encode(prompt))
    completion_tokens = len(tokenizer.encode(response_text))
    
    return ChatCompletionResponse(
        id=f"chatcmpl-{int(time.time())}",
        created=int(time.time()),
        model=MODEL_NAME,
        choices=[
            Choice(
                index=0,
                message=ChatMessage(role="assistant", content=response_text),
                finish_reason="stop"
            )
        ],
        usage=Usage(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens
        )
    )


@app.post("/v1/completions")
async def completions(request: CompletionRequest):
    """Handle text completion requests."""
    
    if request.stream:
        # Streaming response
        return StreamingResponse(
            stream_response(
                request.prompt,
                max_tokens=request.max_tokens,
                temperature=request.temperature,
                top_p=request.top_p,
                top_k=request.top_k
            ),
            media_type="text/event-stream"
        )
    
    # Non-streaming response
    response_text = generate_response(
        request.prompt,
        max_tokens=request.max_tokens,
        temperature=request.temperature,
        top_p=request.top_p,
        top_k=request.top_k
    )
    
    # Calculate token usage
    prompt_tokens = len(tokenizer.encode(request.prompt))
    completion_tokens = len(tokenizer.encode(response_text))
    
    return CompletionResponse(
        id=f"cmpl-{int(time.time())}",
        created=int(time.time()),
        model=MODEL_NAME,
        choices=[
            CompletionChoice(
                index=0,
                text=response_text,
                finish_reason="stop"
            )
        ],
        usage=Usage(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens
        )
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
