# Deployment Guide

## Overview

This guide covers deploying the CPU-only `cogtrix-gemma3-270m` container image in various environments.

## Deployment Options

### 1. Local Deployment

#### Docker Desktop (macOS/Windows/Linux)

```bash
# Build image
docker build -t cogtrix-gemma3-270m .

# Run the OpenAI-compatible server
docker run -p 8080:8080 cogtrix-gemma3-270m
```

#### Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  gemma-3-270m:
    build: .
    image: cogtrix-gemma3-270m:latest
    ports:
      - "8080:8080"
```

Run with:
```bash
docker-compose up
```

### 2. Cloud Deployment

#### AWS EC2

**Prerequisites**:
- EC2 instance sized for CPU inference
- Docker installed

**Setup**:

```bash
# Install Docker
sudo apt update
sudo apt install -y docker.io

# Build and run
docker build -t cogtrix-gemma3-270m .
docker run -p 8080:8080 cogtrix-gemma3-270m
```

#### Google Cloud Platform (GCP)

**Using Cloud Run (CPU-only)**:

```bash
# Build for x86_64
docker build --platform linux/amd64 -t gcr.io/PROJECT_ID/cogtrix-gemma3-270m .

# Push to Artifact Registry
docker push gcr.io/PROJECT_ID/cogtrix-gemma3-270m

# Deploy to Cloud Run
gcloud run deploy gemma-3-270m \
  --image gcr.io/PROJECT_ID/cogtrix-gemma3-270m \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --cpu 4 \
  --memory 8Gi
```

**Using GKE**:

```bash
# Create GKE cluster
gcloud container clusters create gemma-cluster \
  --zone us-central1-a \
  --machine-type e2-standard-4

# Deploy to GKE
kubectl apply -f k8s-deployment.yaml
```

#### Azure Container Instances

```bash
# Build and tag
docker build -t cogtrix-gemma3-270m .
docker tag cogtrix-gemma3-270m YOUR_REGISTRY.azurecr.io/cogtrix-gemma3-270m:latest

# Push to Azure Container Registry
docker push YOUR_REGISTRY.azurecr.io/cogtrix-gemma3-270m:latest

# Deploy to ACI
az container create \
  --resource-group myResourceGroup \
  --name gemma-3-270m \
  --image YOUR_REGISTRY.azurecr.io/cogtrix-gemma3-270m:latest \
  --gpu-count 1 \
  --gpu-vm-size Standard_NC6s_v3 \
  --memory 16 \
  --cpu 4
```

### 3. Kubernetes Deployment

Create `k8s-deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: gemma-3-270m
spec:
  replicas: 1
  selector:
    matchLabels:
      app: gemma-3-270m
  template:
    metadata:
      labels:
        app: gemma-3-270m
    spec:
      containers:
      - name: gemma
        image: cogtrix-gemma3-270m:latest
        command: ["python", "inference.py", "--interactive"]
        resources:
          limits:
            memory: "8Gi"
            cpu: "4000m"
            nvidia.com/gpu: 1
          requests:
            memory: "4Gi"
            cpu: "2000m"
        volumeMounts:
        - name: model-storage
          mountPath: /app/model
      volumes:
      - name: model-storage
        emptyDir: {}
---
apiVersion: v1
kind: Service
metadata:
  name: gemma-3-270m-service
spec:
  selector:
    app: gemma-3-270m
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  type: LoadBalancer
```

Deploy:
```bash
kubectl apply -f k8s-deployment.yaml
```

### 4. Edge Deployment

#### Raspberry Pi 4/5 (aarch64)

```bash
# On Raspberry Pi OS
sudo apt update
sudo apt install -y docker.io

# Build for ARM64
docker build --platform linux/arm64 -t cogtrix-gemma3-270m .

# Run
docker run -it cogtrix-gemma3-270m python inference.py --prompt "Hello"
```

**Note**: Performance will be slower on Raspberry Pi. Consider using quantized models for better performance.

#### ARM Edge Devices

```bash
# Install Docker
sudo apt update
sudo apt install -y docker.io

# Build for ARM64
docker build --platform linux/arm64 -t cogtrix-gemma3-270m .

# Run
docker run -p 8080:8080 cogtrix-gemma3-270m
```

### 5. Production Deployment

#### With API Wrapper

Create `api.py`:

```python
from flask import Flask, request, jsonify
import subprocess
import json

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    prompt = data.get('prompt', 'Hello')
    max_tokens = data.get('max_tokens', 256)
    temperature = data.get('temperature', 0.7)
    
    # Run inference
    result = subprocess.run(
        ['python', 'inference.py', 
         '--prompt', prompt,
         '--max-tokens', str(max_tokens),
         '--temperature', str(temperature)],
        capture_output=True,
        text=True
    )
    
    return jsonify({
        'prompt': prompt,
        'response': result.stdout,
        'status': 'success'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
```

#### Monitoring

Add Prometheus metrics:

```yaml
# docker-compose-monitoring.yml
version: '3.8'

services:
  gemma:
    build: .
    ports:
      - "8080:8080"
    deploy:
      resources:
        limits:
          memory: 8G
          cpus: '4.0'

  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    volumes:
      - grafana-storage:/var/lib/grafana

volumes:
  grafana-storage:
```

## Resource Requirements

### Minimum Requirements

| Resource | Value |
|----------|-------|
| RAM | 4 GB |
| Storage | 2 GB |
| CPU Cores | 2 |

### Recommended Requirements

| Resource | Value |
|----------|-------|
| RAM | 8 GB |
| Storage | 4 GB |
| CPU Cores | 4 |

## Scaling Considerations

### Horizontal Scaling

For high-traffic deployments:

1. **Load Balancing**: Use Kubernetes or cloud load balancer
2. **Multiple Replicas**: Run multiple container instances
3. **Request Queueing**: Implement message queue for request handling

### Vertical Scaling

For complex tasks:

1. **Increase Memory**: Allocate more RAM
2. **Increase CPU**: Allocate more CPU capacity if throughput is insufficient
3. **Optimize Parameters**: Reduce max_tokens for faster response

## Security Best Practices

1. **Non-root User**: Container runs as non-root
2. **Network Isolation**: Use internal networks
3. **Secrets Management**: Use environment variables or secrets manager
4. **Image Scanning**: Regularly scan for vulnerabilities
5. **Resource Limits**: Set CPU and memory limits

## Cost Optimization

1. **Right-size Instances**: Match resources to workload
2. **Spot Instances**: Use spot/preemptible instances for non-critical workloads
3. **Auto-scaling**: Scale based on demand
4. **Caching**: Implement response caching for repeated queries

## Troubleshooting

### Common Issues

**Issue**: Container crashes with OOM
```bash
# Increase memory limit
docker run -m 8g cogtrix-gemma3-270m
```

**Issue**: Slow inference
```bash
# Reduce context size if needed
docker run -e LLAMA_ARG_CTX_SIZE=2048 -p 8080:8080 cogtrix-gemma3-270m

# Reduce max_tokens
docker run cogtrix-gemma3-270m python inference.py --max-tokens 100
```

**Issue**: Model not found
```bash
# Rebuild image to ensure model is included
docker build --no-cache -t cogtrix-gemma3-270m .
```

## Monitoring and Logging

### Docker Logging

```bash
# View logs
docker logs -f gemma-container

# Log to file
docker run --log-driver json-file --log-opt max-size=10m cogtrix-gemma3-270m
```

### Kubernetes Logging

```bash
# View pod logs
kubectl logs -f deployment/gemma-3-270m

# Export logs
kubectl logs deployment/gemma-3-270m > gemma-logs.txt
```

## Next Steps

1. Choose deployment target (local, cloud, edge)
2. Select appropriate resource allocation
3. Configure monitoring and logging
4. Implement security measures
5. Test and validate performance
6. Deploy to production
