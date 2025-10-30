#!/bin/bash

# Test runner script for Users API
# This script runs the test suite with various options

set -e

echo "🧪 Running Users API Test Suite..."
echo ""

# Check if Poetry is available and pyproject.toml exists
if command -v poetry &> /dev/null && [ -f "pyproject.toml" ]; then
    echo "🎭 Using Poetry for testing..."
    
    # Check if test dependencies are installed
    poetry run python -c "import pytest, httpx" 2>/dev/null || {
        echo "❌ Error: Test dependencies not found."
        echo "   Please install dependencies first:"
        echo "   poetry install"
        echo ""
        exit 1
    }
    
    # Remove any existing test database
    rm -f test.db test_*.db
    
    echo "✅ Test dependencies check passed"
    echo "🔧 Running pytest with Poetry..."
    echo ""
    
    # Run tests with coverage if requested
    if [[ "$1" == "--coverage" ]]; then
        echo "📊 Running tests with coverage report..."
        exec poetry run pytest --cov=app --cov-report=html --cov-report=term -v
    elif [[ "$1" == "--watch" ]]; then
        echo "👀 Running tests in watch mode..."
        exec poetry run pytest -f -v
    else
        exec poetry run pytest -v
    fi

else
    echo "📦 Using pip for testing..."
    
    # Check if dependencies are installed
    python -c "import pytest, httpx" 2>/dev/null || {
        echo "❌ Error: Test dependencies not found."
        echo "   Please install test dependencies first:"
        echo "   pip install -r requirements-dev.txt"
        echo ""
        exit 1
    }
    
    # Remove any existing test database
    rm -f test.db test_*.db
    
    echo "✅ Test dependencies check passed"
    echo "🔧 Running pytest..."
    echo ""
    
    # Run tests with coverage if requested
    if [[ "$1" == "--coverage" ]]; then
        echo "📊 Running tests with coverage report..."
        exec pytest --cov=app --cov-report=html --cov-report=term -v
    elif [[ "$1" == "--watch" ]]; then
        echo "👀 Running tests in watch mode..."
        exec pytest -f -v
    else
        exec pytest -v
    fi
fi
