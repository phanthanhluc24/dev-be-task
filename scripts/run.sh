#!/bin/bash

# Users API Development Server Startup Script
# This script starts the FastAPI development server with hot reload enabled

set -e  # Exit on any error

echo "🚀 Starting Users API Development Server..."
echo "📍 Server will be available at: http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/docs"
echo "📖 ReDoc Documentation: http://localhost:8000/redoc"
echo ""

# Check if Poetry is available and pyproject.toml exists
if command -v poetry &> /dev/null && [ -f "pyproject.toml" ]; then
    echo "🎭 Using Poetry for dependency management..."
    
    # Check if dependencies are installed
    poetry run python -c "import fastapi, uvicorn, sqlalchemy, pydantic" 2>/dev/null || {
        echo "❌ Error: Required dependencies not found."
        echo "   Please install dependencies first:"
        echo "   poetry install"
        echo ""
        exit 1
    }
    
    echo "✅ Dependencies check passed"
    echo "🔧 Starting uvicorn server with hot reload..."
    echo ""
    
    # Start the development server with Poetry
    exec poetry run uvicorn app.main:app \
        --reload \
        --host 0.0.0.0 \
        --port 8000 \
        --log-level info

else
    echo "📦 Using pip for dependency management..."
    
    # Check if virtual environment is activated
    if [[ "$VIRTUAL_ENV" == "" ]]; then
        echo "⚠️  Warning: No virtual environment detected."
        echo "   Consider activating a virtual environment first:"
        echo "   source venv/bin/activate"
        echo ""
    fi

    # Check if dependencies are installed
    python -c "import fastapi, uvicorn, sqlalchemy, pydantic" 2>/dev/null || {
        echo "❌ Error: Required dependencies not found."
        echo "   Please install dependencies first:"
        echo "   pip install -r requirements.txt"
        echo ""
        exit 1
    }

    echo "✅ Dependencies check passed"
    echo "🔧 Starting uvicorn server with hot reload..."
    echo ""

    # Start the development server
    exec uvicorn app.main:app \
        --reload \
        --host 0.0.0.0 \
        --port 8000 \
        --log-level info
fi
