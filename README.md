# Users API - Backend Take-Home Challenge

A FastAPI-based REST API starter template for building a simple user management system. This template demonstrates best practices for Python web development using modern tools and patterns.

## 🚀 Features

- **FastAPI** - Modern, fast web framework for building APIs
- **SQLAlchemy 2.x** - Powerful ORM with modern declarative syntax
- **SQLite** - Lightweight database (auto-creates on startup)
- **Pydantic v2** - Data validation and serialization
- **pytest** - Comprehensive testing framework
- **Type hints** - Full typing support throughout the codebase
- **Error handling** - Proper HTTP status codes and error responses

## 📋 Requirements to Implement

Build a REST API with the following endpoints:

### 1. Create User
- **Endpoint**: `POST /users`
- **Request Body**: 
  ```json
  {
    "name": "John Doe",
    "email": "john@example.com"
  }
  ```
- **Response**: Created user with ID and timestamp
- **Validation**: Email must be unique (return 400 if duplicate)

### 2. List Users
- **Endpoint**: `GET /users`
- **Query Parameters**: 
  - `limit` (optional, default: 10) - Number of users to return
  - `offset` (optional, default: 0) - Number of users to skip
- **Response**: List of users with pagination info

## 🛠️ Tech Stack

- **Python 3.10+**
- **FastAPI** - Web framework
- **SQLAlchemy 2.x** - ORM with DeclarativeBase
- **Pydantic v2** - Data validation
- **SQLite** - Database
- **pytest** - Testing
- **uvicorn** - ASGI server

## 📁 Project Structure

```
users-api/
├── README.md              # This file
├── pyproject.toml         # Python project configuration
├── .gitignore            # Git ignore rules
├── app/                  # Main application code
│   ├── __init__.py
│   ├── main.py           # FastAPI app and routes
│   ├── db.py             # Database setup and session management
│   ├── models.py         # SQLAlchemy models
│   ├── schemas.py        # Pydantic request/response schemas
│   └── crud.py           # CRUD operations
├── tests/                # Test files
│   ├── __init__.py
│   └── test_users.py     # API endpoint tests
└── scripts/              # Utility scripts
    └── run.sh            # Development server startup script
```

## 🚀 Getting Started

### Prerequisites
- Python 3.10 or higher
- pip or another Python package manager

### Installation

#### Option 1: Using Poetry (Recommended)

1. **Clone this repository**
   ```bash
   git clone <repository-url>
   cd users-api
   ```

2. **Install Poetry** (if not already installed)
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

3. **Install dependencies**
   ```bash
   poetry install
   ```

4. **Activate the virtual environment**
   ```bash
   poetry shell
   ```

#### Option 2: Using pip

1. **Clone this repository**
   ```bash
   git clone <repository-url>
   cd users-api
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   
   # On Linux/Mac:
   source venv/bin/activate
   
   # On Windows:
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

#### Option 1: Using Poetry
```bash
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Option 2: Using the provided script
```bash
chmod +x scripts/run.sh
./scripts/run.sh
```

#### Option 3: Direct uvicorn command (if using pip)
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔧 Available Commands

### Using Make (Recommended)
```bash
# Show all available commands
make help

# Setup and development
make install-dev    # Install all dependencies
make dev           # Start development server
make test          # Run tests
make test-cov      # Run tests with coverage
make format        # Format code
make lint          # Run linting
make clean         # Clean up cache files
```

### Using Poetry Directly
```bash
poetry install              # Install dependencies
poetry run uvicorn app.main:app --reload  # Start server
poetry run pytest -v       # Run tests
poetry run black app/ tests/  # Format code
poetry run ruff check app/  # Lint code
```

### Using Scripts
```bash
./scripts/run.sh           # Start development server
./scripts/test.sh          # Run tests
./scripts/test.sh --coverage  # Run tests with coverage
```

### Running Tests

#### Using Poetry
```bash
# Run all tests
poetry run pytest

# Run with verbose output
poetry run pytest -v

# Run with coverage
poetry run pytest --cov=app
```

#### Using pip (if virtual environment is activated)
```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=app
```

## 📝 API Documentation

Once the server is running, visit http://localhost:8000/docs for interactive API documentation powered by Swagger UI.

### Example Requests

#### Create a User
```bash
curl -X POST "http://localhost:8000/users" \
     -H "Content-Type: application/json" \
     -d '{"name": "John Doe", "email": "john@example.com"}'
```

#### List Users
```bash
# Get all users
curl "http://localhost:8000/users"

# Get users with pagination
curl "http://localhost:8000/users?limit=5&offset=10"
```

## 🧪 Testing Strategy

The test suite includes:

- **Integration tests** using FastAPI's TestClient
- **Database operations** with test database isolation
- **Error handling** validation (duplicate emails, validation errors)
- **Pagination** functionality testing
- **Type safety** verification

Example test cases:
- ✅ Create user successfully
- ✅ List users with pagination
- ✅ Handle duplicate email error
- ✅ Validate request data
- ✅ Handle edge cases

## 🎯 Evaluation Criteria

Your implementation will be evaluated on:

### 1. **Code Quality** (30%)
- Clean, readable Python code
- Proper use of type hints
- Following Python conventions (PEP 8)
- Good separation of concerns

### 2. **Functionality** (40%)
- All endpoints work as specified
- Proper error handling and HTTP status codes
- Database constraints enforced
- Pagination implemented correctly

### 3. **Testing** (20%)
- Comprehensive test coverage
- Good test structure and organization
- Integration tests with database
- Edge case handling

### 4. **Documentation** (10%)
- Clear README updates
- Code comments where necessary
- API documentation completeness

## 🔧 Development Tips

### Database
- SQLite database file (`users.db`) will be created automatically
- Tables are created on application startup
- Use SQLAlchemy migrations for production applications

### Error Handling
- Return appropriate HTTP status codes
- Provide clear error messages
- Handle database constraints properly

### Testing
- Use FastAPI's TestClient for integration tests
- Test both success and error scenarios
- Verify database state changes

### Type Safety
- Use type hints throughout your code
- Leverage Pydantic for request/response validation
- Enable mypy for static type checking

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy 2.0 Documentation](https://docs.sqlalchemy.org/en/20/)
- [Pydantic Documentation](https://docs.pydantic.dev/2.0/)
- [pytest Documentation](https://docs.pytest.org/)

## 🤝 Submission Guidelines

1. **Fork this repository**
2. **Implement all required features**
3. **Add comprehensive tests**
4. **Update this README** with any additional setup instructions
5. **Ensure all tests pass**
6. **Submit your implementation**

### Submission Checklist
- [ ] `POST /users` endpoint implemented
- [ ] `GET /users` endpoint with pagination
- [ ] Unique email constraint enforced
- [ ] Proper error handling and HTTP status codes
- [ ] Type hints used throughout
- [ ] Tests written and passing
- [ ] Documentation updated

---

**Happy Coding! 🎉**

Built with ❤️ using FastAPI, SQLAlchemy, and modern Python patterns.
