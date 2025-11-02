# Users API - Backend Take-Home Challenge

A FastAPI-based REST API starter template for building a simple user management system. This template demonstrates best practices for Python web development using modern tools and patterns.


## How to run the source manually

1. Create python venv
    > py -m venv .venv

2. Use Venv
    > .\.venv\Scripts\activate

3. Install libs
    > pip install -r requirements.txt

4. Dev run
    > run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000


## How to run pytest
    # Run with verbose output
    pytest -v

    # Run with coverage
    pytest --cov=app


## 🚀 Features

1. **`POST /users`** - Create user with unique email validation
2. **`GET /users`** - List users with pagination (`?limit=&offset=`)
3. **`GET /users/{id}`** - Get individual user by ID (bonus feature)

1. **`POST /users`** – Create a user with unique email validation
2. **`GET /users`** – List users with pagination (?limit=&offset=)
3. **`GET /users/{id}`** – Get individual user by ID (bonus feature)
4. **`PUT /users/{id}`** – Update user (validate unique email, check existence)
5. **`DELETE /users/{id}`** – Delete user by ID


## 📁 Project Structure

```
users-api/
├── README.md              # This file
├── pyproject.toml         # Python project configuration
├── .gitignore            # Git ignore rules
├── app/                  # Main application code
│   ├── __init__.py
│   ├── main.py           # FastAPI app and routes
    ├── controllers/      # Handle HTTP requests, call services, return responses
    ├── repositories/     # CRUD operations, direct DB interaction via models
    ├── models/           # SQLAlchemy models, DB table definitions
    ├── services/         # Business logic, call repositories, enforce rules (e.g., unique email)
    ├── utils/            # Helper functions (date formatting, password hashing, UUIDs, etc.)
    ├── schemas/          # Pydantic models for request validation & response serialization
    ├── exceptions/       # Custom exceptions (e.g., NotFound, Conflict) for consistent error handling
    └── config/           # App configuration & environment variables (DB URL, secrets, settings)
├── tests/                # Test files
│   ├── __init__.py
│   └── test_users.py     # API endpoint tests
└── scripts/              # Utility scripts
    └── run.sh            # Development server startup script
```


