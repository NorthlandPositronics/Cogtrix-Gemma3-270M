#!/usr/bin/env python3
"""
Example Python client for the Gemma 3 270M API.

Demonstrates both non-streaming and streaming API calls.
"""

import requests
import json
import sys


def simple_chat():
    """Simple non-streaming chat example."""
    print("=" * 60)
    print("Simple Chat Example")
    print("=" * 60)
    
    response = requests.post(
        "http://localhost:8080/v1/chat/completions",
        json={
            "model": "gemma-3-270m",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "What is machine learning?"}
            ],
            "temperature": 0.7,
            "max_tokens": 256
        }
    )
    
    result = response.json()
    print(f"\nModel: {result['model']}")
    print(f"Response: {result['choices'][0]['message']['content']}")
    print(f"Tokens: {result['usage']['total_tokens']}")


def streaming_chat():
    """Streaming chat example."""
    print("\n" + "=" * 60)
    print("Streaming Chat Example")
    print("=" * 60)
    
    response = requests.post(
        "http://localhost:8080/v1/chat/completions",
        json={
            "model": "gemma-3-270m",
            "messages": [
                {"role": "user", "content": "Write a short poem about AI"}
            ],
            "temperature": 0.8,
            "max_tokens": 128,
            "stream": True
        },
        stream=True
    )
    
    print("\nResponse (streaming):")
    for line in response.iter_lines():
        if line:
            data = json.loads(line.decode('utf-8').replace('data: ', ''))
            if 'choices' in data and data['choices'][0]['delta'].get('content'):
                print(data['choices'][0]['delta']['content'], end='', flush=True)
    print()


def multi_turn_conversation():
    """Multi-turn conversation example."""
    print("\n" + "=" * 60)
    print("Multi-turn Conversation Example")
    print("=" * 60)
    
    messages = [
        {"role": "system", "content": "You are a coding assistant."},
        {"role": "user", "content": "How do I read a file in Python?"}
    ]
    
    # First turn
    response = requests.post(
        "http://localhost:8080/v1/chat/completions",
        json={
            "model": "gemma-3-270m",
            "messages": messages,
            "temperature": 0.7
        }
    )
    
    result = response.json()
    assistant_response = result['choices'][0]['message']['content']
    print(f"\nAssistant: {assistant_response}")
    
    # Add assistant response to conversation
    messages.append({"role": "assistant", "content": assistant_response})
    
    # Second turn
    messages.append({"role": "user", "content": "Can you show me an example?"})
    
    response = requests.post(
        "http://localhost:8080/v1/chat/completions",
        json={
            "model": "gemma-3-270m",
            "messages": messages,
            "temperature": 0.7
        }
    )
    
    result = response.json()
    print(f"\nAssistant: {result['choices'][0]['message']['content']}")


def text_completion():
    """Text completion example (legacy endpoint)."""
    print("\n" + "=" * 60)
    print("Text Completion Example")
    print("=" * 60)
    
    response = requests.post(
        "http://localhost:8080/v1/completions",
        json={
            "model": "gemma-3-270m",
            "prompt": "Once upon a time",
            "temperature": 0.7,
            "max_tokens": 100
        }
    )
    
    result = response.json()
    print(f"\nPrompt: Once upon a time")
    print(f"Completion: {result['choices'][0]['text']}")


def list_models():
    """List available models."""
    print("\n" + "=" * 60)
    print("List Models")
    print("=" * 60)
    
    response = requests.get("http://localhost:8080/v1/models")
    result = response.json()
    
    print(f"\nAvailable models:")
    for model in result['data']:
        print(f"  - {model['id']} (owned by: {model['owned_by']})")


def check_health():
    """Check API health."""
    print("\n" + "=" * 60)
    print("Health Check")
    print("=" * 60)
    
    response = requests.get("http://localhost:8080/health")
    result = response.json()
    
    print(f"\nStatus: {result['status']}")
    print(f"Model: {result['model']}")


def main():
    """Run all examples."""
    print("Gemma 3 270M API Client Examples")
    print("Make sure the API server is running at http://localhost:8080\n")
    
    try:
        check_health()
        list_models()
        simple_chat()
        streaming_chat()
        multi_turn_conversation()
        text_completion()
        
        print("\n" + "=" * 60)
        print("All examples completed successfully!")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("\nError: Could not connect to the API server.")
        print("Make sure the server is running: python api_server.py")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
