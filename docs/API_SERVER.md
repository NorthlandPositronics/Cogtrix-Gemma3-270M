# OpenAI-Compatible API Server

A CPU-only OpenAI-compatible REST API for Gemma 3 270M. The primary runtime path is `llama.cpp` with a baked-in GGUF model; a legacy FastAPI/PyTorch server remains in the repo.

## Overview

The primary server path exposes the Gemma 3 270M model via HTTP endpoints compatible with the OpenAI API specification. This allows you to:

- Use the model with any OpenAI-compatible client
- Integrate into existing applications expecting OpenAI API
- Test the model in various scenarios without changing your code
- Run as a network service for multiple clients

## Quick Start

### Start the Server

```bash
# Build the fast-start image first
./scripts/build-container-image.sh

# Start the API server
docker run -d -p 8080:8080 cogtrix-gemma3-270m

# Optional: override context size
docker run -d -e LLAMA_ARG_CTX_SIZE=8192 -p 8080:8080 cogtrix-gemma3-270m
```

### Test the API

```bash
# Simple chat request
curl http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemma-3-270m",
    "messages": [
      {"role": "user", "content": "Hello, how are you?"}
    ],
    "temperature": 0.7
  }'
```

## API Endpoints

### Chat Completions

**Endpoint:** `POST /v1/chat/completions`

**Example:**
```bash
curl http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemma-3-270m",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "What is machine learning?"}
    ],
    "temperature": 0.7,
    "max_tokens": 256
  }'
```

**Response:**
```json
{
  "id": "chatcmpl-1711420800",
  "object": "chat.completion",
  "created": 1711420800,
  "model": "gemma-3-270m",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Machine learning is a subset of AI..."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 15,
    "completion_tokens": 42,
    "total_tokens": 57
  }
}
```

### Streaming Response

Enable streaming by setting `"stream": true`:

```bash
curl http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemma-3-270m",
    "messages": [{"role": "user", "content": "Write a poem"}],
    "stream": true
  }'
```

Response is sent as Server-Sent Events (SSE):
```
data: {"id": "chatcmpl-1711420800", "object": "chat.completion.chunk", ...}
data: {"id": "chatcmpl-1711420800", "object": "chat.completion.chunk", ...}
data: [DONE]
```

### List Models

**Endpoint:** `GET /v1/models`

```bash
curl http://localhost:8080/v1/models
```

### Health Check

**Endpoint:** `GET /health`

```bash
curl http://localhost:8080/health
```

## Python Client Examples

### Using Requests

```python
import requests

response = requests.post(
    "http://localhost:8080/v1/chat/completions",
    json={
        "model": "gemma-3-270m",
        "messages": [
            {"role": "user", "content": "Explain quantum computing"}
        ],
        "temperature": 0.7
    }
)

print(response.json()['choices'][0]['message']['content'])
```

### Using OpenAI Python Client

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8080/v1",
    api_key="not-needed"
)

response = client.chat.completions.create(
    model="gemma-3-270m",
    messages=[{"role": "user", "content": "Hello!"}]
)

print(response.choices[0].message.content)
```

## Command Line Options

```bash
python api_server.py [OPTIONS]

Options:
  --host HOST         Host to bind to (default: 0.0.0.0)
  --port PORT         Port to listen on (default: 8080)
  --model-path PATH   Path to model files (default: /app/model)
  --workers NUM       Number of worker processes (default: 1)
```

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| API_HOST | 0.0.0.0 | Host to bind the server |
| API_PORT | 8080 | Port to listen on |
| MODEL_PATH | /app/model | Path to model files |

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| temperature | float | 0.7 | Sampling temperature (0-1) |
| top_p | float | 0.95 | Nucleus sampling parameter |
| top_k | int | 50 | Top-k sampling parameter |
| max_tokens | int | 256 | Maximum tokens to generate |
| stream | boolean | false | Stream the response |

## Running Examples

The `examples/` directory contains ready-to-use examples:

```bash
# Run all examples
python examples/python_client.py

# Run specific example
python -c "
import requests
response = requests.post(
    'http://localhost:8080/v1/chat/completions',
    json={'model': 'gemma-3-270m', 'messages': [{'role': 'user', 'content': 'Hello!'}]}
)
print(response.json()['choices'][0]['message']['content'])
"
```

## Docker Deployment

### Basic Usage

```bash
# Build the fast-start image
./scripts/build-container-image.sh

# Run the API server
docker run -d \
  -p 8080:8080 \
  --name gemma-api \
  cogtrix-gemma3-270m

# Override runtime tuning if needed
docker run -d \
  -p 8080:8080 \
  -e LLAMA_ARG_CTX_SIZE=4096 \
  -e LLAMA_ARG_THREADS=2 \
  -e LLAMA_ARG_THREADS_BATCH=2 \
  -e LLAMA_ARG_BATCH=64 \
  -e LLAMA_ARG_UBATCH=64 \
  -e LLAMA_ARG_PARALLEL=1 \
  -e LLAMA_ARG_FLASH_ATTN=auto \
  -e LLAMA_ARG_NO_WARMUP=1 \
  --name gemma-api \
  cogtrix-gemma3-270m
```

### Production Deployment

```bash
docker run -d \
  -p 8080:8080 \
  --restart unless-stopped \
  --memory 4g \
  --cpus 2 \
  --name gemma-api \
  cogtrix-gemma3-270m
```

## Testing

### Manual Testing

```bash
# Test chat endpoint
curl -X POST http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemma-3-270m",
    "messages": [{"role": "user", "content": "What is the capital of France?"}]
  }'

# Test streaming
curl -X POST http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemma-3-270m",
    "messages": [{"role": "user", "content": "Write a story"}],
    "stream": true
  }'

# Test health check
curl http://localhost:8080/health
```

### Automated Testing

```bash
# Run the example client
python examples/python_client.py
```

## Troubleshooting

### Common Issues

**Issue:** Connection refused
```bash
# Check if the server is running
docker ps | grep gemma-api

# Check logs
docker logs gemma-api
```

**Issue:** Model not found
```bash
# Verify model path
ls -la /path/to/model/

# Ensure model files are present
```

**Issue:** Out of memory
```bash
# Reduce max_tokens
# Lower LLAMA_ARG_CTX_SIZE if needed
# Increase container memory limits
```

## Compatibility

This API is compatible with:

- ✅ OpenAI API specification (chat completions)
- ✅ OpenAI Python client
- ✅ Any HTTP client
- ✅ Streaming (SSE)
- ✅ Multi-turn conversations

## Performance

- **First request**: ~5-10 seconds (model loading)
- **Subsequent requests**: ~1-3 seconds per response
- **Streaming**: Real-time token generation
- **Concurrent requests**: Supported (adjust `--workers`)

## Security Notes

- No authentication by default (add in production)
- Consider adding rate limiting
- Use HTTPS in production
- Restrict network access as needed

## License

MIT License - See LICENSE file for details.
