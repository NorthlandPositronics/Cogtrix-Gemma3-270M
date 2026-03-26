# OpenAI-Compatible API Server

A FastAPI-based server providing an OpenAI-compatible REST API for the Gemma 3 270M model.

## Overview

This API server exposes the Gemma 3 270M model via HTTP endpoints that are compatible with the OpenAI API specification. This allows you to:

- Use the model with any OpenAI-compatible client
- Integrate into existing applications expecting OpenAI API
- Test the model in various scenarios without changing your code
- Run as a network service for multiple clients

## Quick Start

### Start the Server

```bash
# Build the container first (if not done)
./build.sh

# Start the API server
docker run -d \
  -p 8080:8080 \
  -v ./model:/app/model \
  gemma-3-270m-minimal \
  python api_server.py --host 0.0.0.0 --port 8080
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
# Build the image
./build.sh

# Run the API server
docker run -d \
  -p 8080:8080 \
  -v ./model:/app/model \
  --name gemma-api \
  gemma-3-270m-minimal \
  python api_server.py --host 0.0.0.0 --port 8080
```

### Production Deployment

```bash
docker run -d \
  -p 8080:8080 \
  -v ./model:/app/model \
  --restart unless-stopped \
  --memory 4g \
  --cpus 2 \
  --name gemma-api \
  gemma-3-270m-minimal \
  python api_server.py --host 0.0.0.0 --port 8080 --workers 2
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
# Use CPU instead of GPU if needed
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
