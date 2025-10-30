# Users API - Makefile for common development tasks
# Use 'make help' to see available commands

.PHONY: help install install-dev dev test test-cov lint format clean docker-build docker-run

# Default target
help:
	@echo "🚀 Users API - Available Commands"
	@echo ""
	@echo "📦 Setup:"
	@echo "  install      Install production dependencies with Poetry"
	@echo "  install-dev  Install all dependencies (including dev) with Poetry"
	@echo ""
	@echo "🏃 Development:"
	@echo "  dev          Start development server with hot reload"
	@echo "  test         Run test suite"
	@echo "  test-cov     Run tests with coverage report"
	@echo ""
	@echo "🔧 Code Quality:"
	@echo "  lint         Run linting checks (ruff, mypy)"
	@echo "  format       Format code (black, isort)"
	@echo "  check        Run all quality checks (lint + format check)"
	@echo ""
	@echo "🐳 Docker:"
	@echo "  docker-build Build Docker image"
	@echo "  docker-run   Run Docker container"
	@echo ""
	@echo "🧹 Cleanup:"
	@echo "  clean        Remove cache files and databases"

# Installation
install:
	@echo "📦 Installing production dependencies..."
	poetry install --only=main

install-dev:
	@echo "📦 Installing all dependencies (including dev)..."
	poetry install

# Development
dev:
	@echo "🚀 Starting development server..."
	poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Testing
test:
	@echo "🧪 Running test suite..."
	@rm -f test.db test_*.db
	poetry run pytest -v

test-cov:
	@echo "📊 Running tests with coverage..."
	@rm -f test.db test_*.db
	poetry run pytest --cov=app --cov-report=html --cov-report=term -v
	@echo "📈 Coverage report generated in htmlcov/"

# Code quality
lint:
	@echo "🔍 Running linting checks..."
	poetry run ruff check app/ tests/
	poetry run mypy app/

format:
	@echo "✨ Formatting code..."
	poetry run black app/ tests/
	poetry run isort app/ tests/

check: format lint
	@echo "✅ All quality checks completed"

# Docker
docker-build:
	@echo "🐳 Building Docker image..."
	docker build -t users-api .

docker-run:
	@echo "🐳 Running Docker container..."
	docker run -p 8000:8000 --name users-api-container users-api

# Cleanup
clean:
	@echo "🧹 Cleaning up..."
	@rm -rf __pycache__/
	@rm -rf app/__pycache__/
	@rm -rf tests/__pycache__/
	@rm -rf .pytest_cache/
	@rm -rf htmlcov/
	@rm -rf .coverage
	@rm -f test.db test_*.db users.db
	@rm -rf .mypy_cache/
	@rm -rf .ruff_cache/
	@echo "✅ Cleanup completed"

# Install pre-commit hooks (optional)
install-hooks:
	@echo "🪝 Installing pre-commit hooks..."
	poetry run pre-commit install

# Show project info
info:
	@echo "📋 Project Information:"
	@echo "  Poetry version: $$(poetry --version)"
	@echo "  Python version: $$(poetry run python --version)"
	@echo "  Virtual env: $$(poetry env info --path)"
	@poetry show --tree
