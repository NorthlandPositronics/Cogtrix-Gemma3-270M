# API Reference

Gemma 3 270M OpenAI-Compatible API

## Overview

The API server provides an OpenAI-compatible interface for the Gemma 3 270M model, allowing you to use it as a drop-in replacement in applications expecting the OpenAI API.

## Base URL

```
http://localhost:8080
```

## Authentication

Currently no authentication is required for local deployment. Add authentication in production environments.

## Endpoints

### GET /v1/models

List available models.

**Request:**
```bash
curl http://localhost:8080/v1/models
```

**Response:**
```json
{
  "object": "list",
  "data": [
    {
      "id": "gemma-3-270m",
      "object": "model",
      "owned_by": "gemma",
      "created": 1711420800
    }
  ]
}
```

### POST /v1/chat/completions

Generate chat completions using the model.

**Request:**
```bash
curl http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemma-3-270m",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "Hello, how are you?"}
    ],
    "temperature": 0.7,
    "max_tokens": 256
  }'
```

**Request Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| model | string | "gemma-3-270m" | Model ID to use |
| messages | array | Required | List of messages with role and content |
| temperature | float | 0.7 | Sampling temperature (0-1) |
| top_p | float | 0.95 | Nucleus sampling parameter |
| top_k | int | 50 | Top-k sampling parameter |
| max_tokens | int | 256 | Maximum tokens to generate |
| stream | boolean | false | Whether to stream the response |
| n | int | 1 | Number of completions to generate |

**Response (Non-streaming):**
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
        "content": "Hello! I'm doing well, thank you for asking. How can I help you today?"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 15,
    "completion_tokens": 20,
    "total_tokens": 35
  }
}
```

**Response (Streaming):**

The server returns Server-Sent Events (SSE) with the format:
```
data: {"id": "chatcmpl-1711420800", "object": "chat.completion.chunk", "created": 1711420800, "model": "gemma-3-270m", "choices": [{"delta": {"content": "Hello"}, "index": 0, "finish_reason": null}]}

data: {"id": "chatcmpl-1711420800", "object": "chat.completion.chunk", "created": 1711420800, "model": "gemma-3-270m", "choices": [{"delta": {"content": "!"}, "index": 0, "finish_reason": null}]}

data: [DONE]
```

### POST /v1/completions

Generate text completions (legacy endpoint).

**Request:**
```bash
curl http://localhost:8080/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemma-3-270m",
    "prompt": "Once upon a time",
    "temperature": 0.7,
    "max_tokens": 100
  }'
```

**Response:**
```json
{
  "id": "cmpl-1711420800",
  "object": "text_completion",
  "created": 1711420800,
  "model": "gemma-3-270m",
  "choices": [
    {
      "text": " , there was a beautiful princess who lived in a castle...",
      "index": 0,
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 4,
    "completion_tokens": 12,
    "total_tokens": 16
  }
}
```

### GET /health

Health check endpoint.

**Request:**
```bash
curl http://localhost:8080/health
```

**Response:**
```json
{
  "status": "healthy",
  "model": "gemma-3-270m"
}
```

## Message Roles

The chat completions endpoint supports three message roles:

| Role | Description |
|------|-------------|
| `system` | System-level instructions for the model |
| `user` | User input/messages |
| `assistant` | Model responses (for multi-turn conversations) |

**Example Multi-turn Conversation:**
```json
{
  "model": "gemma-3-270m",
  "messages": [
    {"role": "system", "content": "You are a helpful coding assistant."},
    {"role": "user", "content": "How do I read a file in Python?"},
    {"role": "assistant", "content": "You can read a file using the open() function..."},
    {"role": "user", "content": "Can you show me an example?"}
  ]
}
```

## Python Client Example

```python
import requests
import json

# Non-streaming request
response = requests.post(
    "http://localhost:8080/v1/chat/completions",
    json={
        "model": "gemma-3-270m",
        "messages": [
            {"role": "user", "content": "Explain quantum computing"}
        ],
        "temperature": 0.7,
        "max_tokens": 512
    }
)

result = response.json()
print(result['choices'][0]['message']['content'])

# Streaming request
response = requests.post(
    "http://localhost:8080/v1/chat/completions",
    json={
        "model": "gemma-3-270m",
        "messages": [
            {"role": "user", "content": "Write a story"}
        ],
        "stream": True
    },
    stream=True
)

for line in response.iter_lines():
    if line:
        data = json.loads(line.decode('utf-8').replace('data: ', ''))
        if 'choices' in data and data['choices'][0]['delta'].get('content'):
            print(data['choices'][0]['delta']['content'], end='')
```

## OpenAI Python Client Example

```python
from openai import OpenAI

# Configure client to use local server
client = OpenAI(
    base_url="http://localhost:8080/v1",
    api_key="not-needed"  # Not required for local deployment
)

# Chat completion
response = client.chat.completions.create(
    model="gemma-3-270m",
    messages=[
        {"role": "user", "content": "What is the capital of France?"}
    ],
    temperature=0.7
)

print(response.choices[0].message.content)
```

## Error Handling

The API returns standard HTTP status codes:

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad Request - Invalid parameters |
| 422 | Validation Error - Request body validation failed |
| 500 | Internal Server Error - Model inference failed |

**Error Response:**
```json
{
  "detail": "Error message describing the issue"
}
```

## Rate Limiting

Currently, there is no built-in rate limiting. Add middleware in production environments.

## Performance Considerations

- **First request**: May be slower as the model loads into memory
- **Subsequent requests**: Faster as model is cached
- **Streaming**: Recommended for better user experience with long responses
- **Batching**: Multiple concurrent requests are supported

## Docker Usage

```bash
# Start the API server in a container
docker run -d \
  -p 8080:8080 \
  -v ./model:/app/model \
  cogtrix-gemma3-270m \
  python api_server.py --host 0.0.0.0 --port 8080

# Test the API
curl http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemma-3-270m",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| API_HOST | 0.0.0.0 | Host to bind the server |
| API_PORT | 8080 | Port to listen on |
| MODEL_PATH | /app/model | Path to model files |
