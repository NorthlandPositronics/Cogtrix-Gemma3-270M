# Gemma 3 270M Minimal Container Makefile
# Requires HF_TOKEN env var — model weights are downloaded at build time.

IMAGE_NAME := gemma-3-270m-minimal
VERSION := $(shell cat VERSION 2>/dev/null || echo "latest")

.PHONY: help build run api test shell clean

help:
	@echo "Gemma 3 270M Minimal Container"
	@echo ""
	@echo "Available targets:"
	@echo "  build     - Build the Docker image (requires HF_TOKEN)"
	@echo "  run       - Run inference interactively"
	@echo "  api       - Start the API server on port 8080"
	@echo "  test      - Run inference tests inside the container"
	@echo "  shell     - Open a shell in the container"
	@echo "  clean     - Remove the local image"
	@echo ""
	@echo "Example:"
	@echo "  export HF_TOKEN=hf_..."
	@echo "  make build && make api"

build:
	@if [ -z "$$HF_TOKEN" ]; then \
	    echo "ERROR: HF_TOKEN is not set. See scripts/build.sh for instructions."; \
	    exit 1; \
	fi
	@echo "Building $(IMAGE_NAME):$(VERSION) (downloading model weights)..."
	DOCKER_BUILDKIT=1 docker build \
	    --secret id=hf_token,env=HF_TOKEN \
	    -t $(IMAGE_NAME):$(VERSION) \
	    -f docker/Dockerfile \
	    .

run: build
	docker run -it $(IMAGE_NAME):$(VERSION) python src/inference.py --interactive

api: build
	docker run -p 8080:8080 $(IMAGE_NAME):$(VERSION) python src/api_server.py

test: build
	docker run --rm $(IMAGE_NAME):$(VERSION) python src/test_inference.py

shell: build
	docker run -it $(IMAGE_NAME):$(VERSION) /bin/bash

clean:
	@echo "Cleaning up..."
	docker rmi -f $(IMAGE_NAME):$(VERSION) 2>/dev/null || true
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "Done!"
