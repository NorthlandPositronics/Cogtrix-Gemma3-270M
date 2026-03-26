# Gemma 3 270M Minimal Container Makefile

IMAGE_NAME := gemma-3-270m-minimal
VERSION := $(shell cat VERSION 2>/dev/null || echo "latest")

.PHONY: help build run test api clean

help:
	@echo "Gemma 3 270M Minimal Container"
	@echo ""
	@echo "Available targets:"
	@echo "  build     - Build the Docker image"
	@echo "  run       - Run inference interactively"
	@echo "  api       - Start the API server"
	@echo "  test      - Run inference tests"
	@echo "  shell     - Open a shell in the container"
	@echo "  clean     - Remove build artifacts"

build:
	@echo "Building $(IMAGE_NAME):$(VERSION)..."
	docker build -t $(IMAGE_NAME):$(VERSION) -f docker/Dockerfile .

run: build
	docker run -it $(IMAGE_NAME):$(VERSION) python src/inference.py --interactive

api: build
	docker run -p 8080:8080 $(IMAGE_NAME):$(VERSION) python src/api_server.py

test: build
	docker run -it $(IMAGE_NAME):$(VERSION) python src/test_inference.py

shell: build
	docker run -it $(IMAGE_NAME):$(VERSION) /bin/sh

clean:
	@echo "Cleaning up..."
	docker rmi -f $(IMAGE_NAME):$(VERSION) 2>/dev/null || true
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "Done!"
