# Define variables
VENV_DIR := .venv
DOCKER_IMAGE := picpay-case
PYTHON := $(VENV_DIR)/bin/python
PIP := $(VENV_DIR)/bin/pip

# Default target
default: test

# Create virtual environment
venv:
	@echo "Creating virtual environment..."
	python3 -m venv $(VENV_DIR)

# Install requirements
install:
	@echo "Installing requirements..."
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

# Build Docker image
build:
	@echo "Building Docker image..."
	docker build -t $(DOCKER_IMAGE) .

# Run main.py
run:
	@echo "Running src/main.py..."
	$(PYTHON) src/main.py

# Run the Docker container
launch:
	@echo "Running Docker container..."
	docker run -p 8080:8080 -v /tmp:/tmp $(DOCKER_IMAGE)

# Run tests with pytest
test:
	@echo "Running tests with pytest..."
	$(PYTHON) -m pytest ./tests