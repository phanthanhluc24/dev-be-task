# Contributing to Users API

Thank you for your interest in contributing to the Users API project! This document provides guidelines and information for contributors.

## 🚀 Quick Start for Contributors

### 1. Fork and Clone
```bash
git clone https://github.com/your-username/users-api.git
cd users-api
```

### 2. Set Up Development Environment

#### Using Poetry (Recommended)
```bash
# Install Poetry (if not already installed)
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install

# Activate virtual environment
poetry shell
```

#### Using pip
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 3. Run Tests

#### Using Poetry
```bash
# Run all tests
poetry run pytest -v

# Run with coverage
poetry run pytest --cov=app --cov-report=html

# Run specific test file
poetry run pytest tests/test_users.py -v
```

#### Using pip (with virtual environment activated)
```bash
# Run all tests
pytest -v

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_users.py -v
```

### 4. Start Development Server

#### Using Poetry
```bash
# Using Poetry directly
poetry run uvicorn app.main:app --reload

# Or using the script
./scripts/run.sh
```

#### Using pip (with virtual environment activated)
```bash
# Using the script
./scripts/run.sh

# Or directly
uvicorn app.main:app --reload
```

## 🧪 Testing Guidelines

### Writing Tests
- Place tests in the `tests/` directory
- Use descriptive test names that explain what is being tested
- Follow the Arrange-Act-Assert pattern
- Test both success and error cases
- Use fixtures for common setup

### Test Categories
- **Unit Tests**: Test individual functions and classes
- **Integration Tests**: Test API endpoints end-to-end
- **Edge Cases**: Test boundary conditions and error handling

### Example Test Structure
```python
class TestUserCreation:
    """Test user creation functionality."""
    
    def test_create_user_success(self, test_client):
        """Test successful user creation with valid data."""
        # Arrange
        user_data = {"name": "John Doe", "email": "john@example.com"}
        
        # Act
        response = test_client.post("/users", json=user_data)
        
        # Assert
        assert response.status_code == 201
        assert response.json()["email"] == user_data["email"]
```

## 📝 Code Style Guidelines

### Python Code Style
- Follow PEP 8 conventions
- Use type hints for all function parameters and return values
- Write docstrings for classes and functions
- Keep functions small and focused
- Use meaningful variable and function names

### Code Formatting
We use automated tools for consistent formatting:

#### Using Poetry
```bash
# Format code with Black
poetry run black app/ tests/

# Sort imports with isort
poetry run isort app/ tests/

# Lint with Ruff
poetry run ruff check app/ tests/

# Type checking with mypy
poetry run mypy app/
```

#### Using pip (with virtual environment activated)
```bash
# Format code with Black
black app/ tests/

# Sort imports with isort
isort app/ tests/

# Lint with Ruff
ruff check app/ tests/

# Type checking with mypy
mypy app/
```

### Commit Messages
Use conventional commit format:
```
feat: add user deletion endpoint
fix: handle duplicate email error correctly
docs: update API documentation
test: add pagination tests
refactor: improve error handling
```

## 🏗️ Project Structure

```
users-api/
├── app/                    # Main application code
│   ├── __init__.py
│   ├── main.py            # FastAPI app and routes
│   ├── db.py              # Database configuration
│   ├── models.py          # SQLAlchemy models
│   ├── schemas.py         # Pydantic schemas
│   └── crud.py            # Database operations
├── tests/                 # Test files
│   ├── __init__.py
│   └── test_users.py      # API tests
├── scripts/               # Utility scripts
│   ├── run.sh            # Development server
│   └── test.sh           # Test runner
└── docs/                 # Documentation (if added)
```

## 🔧 Development Workflow

### 1. Feature Development
1. Create a feature branch: `git checkout -b feature/your-feature-name`
2. Write tests for your feature
3. Implement the feature
4. Ensure all tests pass
5. Update documentation if needed
6. Submit a pull request

### 2. Bug Fixes
1. Create a bug fix branch: `git checkout -b fix/bug-description`
2. Write a test that reproduces the bug
3. Fix the bug
4. Ensure the test passes and no regressions occur
5. Submit a pull request

### 3. Before Submitting PR

#### Using Poetry
```bash
# Run full test suite
poetry run pytest -v

# Check code formatting
poetry run black --check app/ tests/
poetry run isort --check-only app/ tests/

# Run linting
poetry run ruff check app/ tests/

# Type checking
poetry run mypy app/
```

#### Using pip (with virtual environment activated)
```bash
# Run full test suite
pytest -v

# Check code formatting
black --check app/ tests/
isort --check-only app/ tests/

# Run linting
ruff check app/ tests/

# Type checking
mypy app/
```

## 📋 Implementation Checklist

When implementing new features, consider:

- [ ] **Functionality**: Does it work as expected?
- [ ] **Tests**: Are there comprehensive tests?
- [ ] **Documentation**: Is it documented?
- [ ] **Error Handling**: Are edge cases handled?
- [ ] **Type Safety**: Are type hints used?
- [ ] **Performance**: Is it performant?
- [ ] **Security**: Are there security considerations?

## 🤝 Pull Request Guidelines

### Before Submitting
- Ensure all tests pass
- Add tests for new functionality
- Update documentation
- Follow code style guidelines
- Write a clear PR description

### PR Description Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing
- [ ] Tests added/updated
- [ ] All tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
```

## 🐛 Bug Reports

When reporting bugs, please include:
- Steps to reproduce
- Expected behavior
- Actual behavior
- Error messages/logs
- Environment details (Python version, OS, etc.)

## 💡 Feature Requests

For feature requests, please provide:
- Clear description of the feature
- Use case/motivation
- Proposed implementation (if any)
- Alternatives considered

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pytest Documentation](https://docs.pytest.org/)
- [PEP 8 Style Guide](https://pep8.org/)

## 🏆 Recognition

Contributors are recognized in our README.md file. Thank you for helping make this project better!

---

Happy contributing! 🎉
