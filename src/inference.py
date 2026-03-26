#!/usr/bin/env python3
"""
Gemma 3 270M Inference Script (CPU-Only)

A minimal inference script for the Gemma 3 270M model optimized for CPU-only execution.
This version removes all GPU/MPS detection logic for maximum compatibility and minimal dependencies.

Usage:
    python inference.py --prompt "Your prompt here"
    python inference.py --interactive
    python inference.py --prompt "Hello" --max-tokens 100 --temperature 0.7
"""

import argparse
import sys
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Run CPU-only inference with Gemma 3 270M model"
    )
    parser.add_argument(
        "--prompt",
        type=str,
        default="Hello, how can I assist you today?",
        help="Input prompt for the model (default: 'Hello, how can I assist you today?')"
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=256,
        help="Maximum number of tokens to generate (default: 256)"
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.7,
        help="Sampling temperature (default: 0.7, range: 0.0-2.0)"
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=50,
        help="Top-k sampling parameter (default: 50)"
    )
    parser.add_argument(
        "--top-p",
        type=float,
        default=0.95,
        help="Top-p (nucleus) sampling parameter (default: 0.95)"
    )
    parser.add_argument(
        "--do-sample",
        action="store_true",
        help="Use sampling instead of greedy decoding"
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Run in interactive mode"
    )
    parser.add_argument(
        "--model-path",
        type=str,
        default="/app/data/model",
        help="Path to the model directory (default: /app/data/model)"
    )
    parser.add_argument(
        "--num-threads",
        type=int,
        default=4,
        help="Number of CPU threads to use (default: 4)"
    )
    return parser.parse_args()


def get_device():
    """Return CPU device (CPU-only build)."""
    device = torch.device("cpu")
    print("✓ CPU-only inference mode")
    print(f"  PyTorch version: {torch.__version__}")
    print(f"  CPU count: {torch.get_num_threads()}")
    return device


def load_model(model_path, device, num_threads=4):
    """Load the model and tokenizer for CPU inference."""
    print(f"\nLoading model on CPU (using {num_threads} threads)...")
    
    # Set number of threads
    torch.set_num_threads(num_threads)
    
    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(
        model_path,
        trust_remote_code=True
    )
    
    # Load model optimized for CPU
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        torch_dtype=torch.float32,  # Use float32 for CPU
        device_map="cpu",
        low_cpu_mem_usage=True,
        trust_remote_code=True
    )
    
    # Set model to evaluation mode
    model.eval()
    
    print("✓ Model loaded successfully!")
    print(f"  Model size: ~{model.get_memory_footprint() / 1024 / 1024:.0f} MB")
    return model, tokenizer


def generate_response(
    model,
    tokenizer,
    prompt,
    device,
    max_tokens=256,
    temperature=0.7,
    top_k=50,
    top_p=0.95,
    do_sample=False
):
    """Generate a response from the model."""
    
    # Tokenize input
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    input_length = inputs["input_ids"].shape[1]
    
    # Configure generation parameters
    gen_kwargs = {
        "max_new_tokens": max_tokens,
        "do_sample": do_sample or temperature != 1.0,
        "temperature": temperature,
        "top_k": top_k,
        "top_p": top_p,
        "pad_token_id": tokenizer.eos_token_id,
    }
    
    # Generate response
    with torch.no_grad():
        outputs = model.generate(**inputs, **gen_kwargs)
    
    # Decode response
    response = tokenizer.decode(
        outputs[0][input_length:],
        skip_special_tokens=True
    )
    
    return response.strip()


def run_interactive(model, tokenizer, device):
    """Run the model in interactive mode."""
    print("\n" + "=" * 60)
    print("  Interactive Mode - Type 'quit' or 'exit' to end")
    print("=" * 60 + "\n")
    
    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()
            
            if user_input.lower() in ["quit", "exit", "q"]:
                print("\nGoodbye!")
                break
            
            if not user_input:
                continue
            
            # Generate response
            print("\nGemma 3 270M: ", end="", flush=True)
            response = generate_response(
                model,
                tokenizer,
                user_input,
                device,
                max_tokens=512,
                temperature=0.7,
                do_sample=True
            )
            print(response)
            print()
            
        except KeyboardInterrupt:
            print("\n\nInterrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}\n")


def main():
    """Main function."""
    args = parse_args()
    
    print("=" * 60)
    print("  Gemma 3 270M - Minimal CPU-Only Container")
    print("=" * 60)
    
    # Detect device (CPU-only)
    device = get_device()
    
    # Load model
    model, tokenizer = load_model(args.model_path, device, args.num_threads)
    
    if args.interactive:
        # Interactive mode
        run_interactive(model, tokenizer, device)
    else:
        # Single prompt mode
        print(f"\nInput: {args.prompt}\n")
        print("Generating response...\n")
        
        response = generate_response(
            model,
            tokenizer,
            args.prompt,
            device,
            max_tokens=args.max_tokens,
            temperature=args.temperature,
            top_k=args.top_k,
            top_p=args.top_p,
            do_sample=args.do_sample
        )
        
        print(f"Output: {response}\n")
    
    print("=" * 60)
    print("  Inference complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
