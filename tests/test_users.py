"""
Integration tests for the Users API endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config.database import Base, get_db
from app.main import app

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# Override the dependency
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def test_client():
    """
    Create a test client with a fresh database for each test.
    """
    # Create tables
    Base.metadata.create_all(bind=engine)

    with TestClient(app) as client:
        yield client

    # Drop tables after test
    Base.metadata.drop_all(bind=engine)


class TestHealthCheck:
    """Test health check endpoint."""

    def test_root_endpoint(self, test_client: TestClient):
        """Test the root health check endpoint."""
        response = test_client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert data["message"] == "Users API is running!"


class TestCreateUser:
    """Test user creation endpoint."""

    def test_create_user_success(self, test_client: TestClient):
        """Test successful user creation."""
        user_data = {"name": "John Doe", "email": "john.doe@example.com"}

        response = test_client.post("/users", json=user_data)
        assert response.status_code == 201

        resp = response.json()

        assert resp["status"] == "success"
        assert resp["message"] == "Created"
        assert "data" in resp

        data = resp["data"]

        assert data["name"] == user_data["name"]
        assert data["email"] == user_data["email"]

        assert "id" in data
        assert "created_at" in data
        assert data["updated_at"] is None

    def test_create_user_duplicate_email(self, test_client: TestClient):
        """Test creating user with duplicate email returns 400."""
        user_data = {"name": "John Doe", "email": "john.doe@example.com"}

        # Create first user
        response1 = test_client.post("/users", json=user_data)
        assert response1.status_code == 201

        # Try to create user with same email
        user_data2 = {"name": "Jane Doe", "email": "john.doe@example.com"}  # Same email
        response2 = test_client.post("/users", json=user_data2)
        assert response2.status_code == 409

        data = response2.json()
        assert "already exists" in data["message"]

    def test_create_user_invalid_email(self, test_client: TestClient):
        """Test creating user with invalid email format."""
        user_data = {"name": "John Doe", "email": "invalid-email"}

        response = test_client.post("/users", json=user_data)
        assert response.status_code == 422

    def test_create_user_missing_fields(self, test_client: TestClient):
        """Test creating user with missing required fields."""
        # Missing email
        user_data = {"name": "John Doe"}
        response = test_client.post("/users", json=user_data)
        assert response.status_code == 422

        # Missing name
        user_data = {"email": "john@example.com"}
        response = test_client.post("/users", json=user_data)
        assert response.status_code == 422

    def test_create_user_empty_name(self, test_client: TestClient):
        """Test creating user with empty name."""
        user_data = {"name": "", "email": "john@example.com"}

        response = test_client.post("/users", json=user_data)
        assert response.status_code == 422


class TestListUsers:
    """Test user listing endpoint."""

    def test_list_users_empty(self, test_client: TestClient):
        """Test listing users when database is empty."""
        response = test_client.get("/users")
        assert response.status_code == 200

        data = response.json()
        assert data["data"]["users"] == []
        assert data["data"]["total"] == 0
        assert data["data"]["limit"] == 10
        assert data["data"]["offset"] == 0

    def test_list_users_with_data(self, test_client: TestClient):
        """Test listing users with data in database."""
        # Create test users
        users_data = [
            {"name": "John Doe", "email": "john@example.com"},
            {"name": "Jane Smith", "email": "jane@example.com"},
            {"name": "Bob Johnson", "email": "bob@example.com"},
        ]

        for user_data in users_data:
            response = test_client.post("/users", json=user_data)
            assert response.status_code == 201

        # List users
        response = test_client.get("/users")
        assert response.status_code == 200

        resp = response.json()

        assert resp["status"] == "success"
        assert resp["message"] == "Success"
        assert "data" in resp

        data = resp["data"]

        assert "users" in data
        assert len(data["users"]) == 3
        assert data["total"] == 3
        assert data["limit"] == 10
        assert data["offset"] == 0

        returned_names = [user["name"] for user in data["users"]]
        assert "Bob Johnson" in returned_names

        user_names = [user["name"] for user in data["users"]]
        assert "Bob Johnson" in user_names  # Last created should be first

    def test_list_users_pagination(self, test_client: TestClient):
        """Test user listing with pagination parameters."""
        # Create 15 test users
        for i in range(15):
            user_data = {"name": f"User {i}", "email": f"user{i}@example.com"}
            response = test_client.post("/users", json=user_data)
            assert response.status_code == 201

        # ==== First page ====
        response = test_client.get("/users?limit=5&offset=0")
        assert response.status_code == 200
        resp = response.json()

        assert resp["status"] == "success"
        assert "data" in resp
        data = resp["data"]

        assert len(data["users"]) == 5
        assert data["total"] == 15
        assert data["limit"] == 5
        assert data["offset"] == 0

        # ==== Second page ====
        response = test_client.get("/users?limit=5&offset=5")
        assert response.status_code == 200
        resp = response.json()
        data = resp["data"]

        assert len(data["users"]) == 5
        assert data["total"] == 15
        assert data["limit"] == 5
        assert data["offset"] == 5

        # ==== Last page ====
        response = test_client.get("/users?limit=5&offset=10")
        assert response.status_code == 200
        resp = response.json()
        data = resp["data"]

        assert len(data["users"]) == 5
        assert data["total"] == 15

    def test_list_users_invalid_pagination(self, test_client: TestClient):
        """Test user listing with invalid pagination parameters."""
        # Negative offset
        response = test_client.get("/users?offset=-1")
        assert response.status_code == 422

        # Limit too large
        response = test_client.get("/users?limit=101")
        assert response.status_code == 422

        # Limit too small
        response = test_client.get("/users?limit=0")
        assert response.status_code == 422


class TestGetUser:
    """Test individual user retrieval endpoint."""

    def test_get_user_success(self, test_client: TestClient):
        """Test successful user retrieval by ID."""
        # Create a user first
        user_data = {"name": "John Doe", "email": "john@example.com"}
        create_response = test_client.post("/users", json=user_data)
        assert create_response.status_code == 201

        created = create_response.json()
        created_id = created["data"]["id"]

        # Get the user by ID
        response = test_client.get(f"/users/{created_id}")
        assert response.status_code == 200

        resp = response.json()
        assert resp["status"] == "success"
        assert "data" in resp

        data = resp["data"]

        assert data["id"] == created_id
        assert data["name"] == user_data["name"]
        assert data["email"] == user_data["email"]

    def test_get_user_not_found(self, test_client: TestClient):
        """Test getting user that doesn't exist."""
        response = test_client.get("/users/999")
        assert response.status_code == 404

        data = response.json()
        assert "not found" in data["message"]


class TestUpdateUser:
    """Test updating user endpoint."""

    def test_update_user_success(self, test_client: TestClient):
        """Test successful user update."""
        # Create initial user
        user_data = {"name": "John Doe", "email": "john@example.com"}
        create_response = test_client.post("/users", json=user_data)
        assert create_response.status_code == 201

        created = create_response.json()
        created_id = created["data"]["id"]

        # Update only the name
        update_data = {"name": "Johnny", "email": created["data"]["email"]}
        update_response = test_client.put(f"/users/{created_id}", json=update_data)
        assert update_response.status_code == 200

        updated = update_response.json()
        data = updated["data"]

        assert data["id"] == created_id
        assert data["name"] == "Johnny"
        assert data["email"] == "john@example.com"
        assert data["updated_at"] is not None

    def test_update_user_duplicate_email(self, test_client: TestClient):
        """Test updating user with existing email should fail."""
        # Create user A
        user_a = {"name": "User A", "email": "a@example.com"}
        res_a = test_client.post("/users", json=user_a)
        assert res_a.status_code == 201

        # Create user B
        user_b = {"name": "User B", "email": "b@example.com"}
        res_b = test_client.post("/users", json=user_b)
        assert res_b.status_code == 201
        created_b = res_b.json()["data"]

        update_data = {"name": "User B2", "email": "a@example.com"}
        update_response = test_client.put(f"/users/{created_b['id']}", json=update_data)
        assert update_response.status_code == 409

        data = update_response.json()
        assert "already exists" in data["message"]

    def test_update_user_not_found(self, test_client: TestClient):
        """Updating a non-existing user should return 404."""
        update_data = {"name": "Ghost", "email": "ghost@example.com"}
        response = test_client.put("/users/999", json=update_data)

        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["message"]


class TestDeleteUser:
    """Test user deletion endpoint."""

    def test_delete_user_success(self, test_client: TestClient):
        """Test successfully deleting a user."""
        # Create user
        user_data = {"name": "To Delete", "email": "del@example.com"}
        create_res = test_client.post("/users", json=user_data)
        assert create_res.status_code == 201
        created = create_res.json()["data"]

        # Delete user
        delete_res = test_client.delete(f"/users/{created['id']}")
        assert delete_res.status_code == 200

        data = delete_res.json()
        assert "success" in data["status"].lower()

        list_res = test_client.get("/users")
        list_data = list_res.json()["data"]
        users = list_data["users"]

        assert all(u["id"] != created["id"] for u in users)

    def test_delete_user_not_found(self, test_client: TestClient):
        """Deleting non-existing user should return 404."""
        response = test_client.delete("/users/999")

        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["message"]


class TestAPIDocumentation:
    """Test API documentation endpoints."""

    def test_openapi_schema(self, test_client: TestClient):
        """Test that OpenAPI schema is accessible."""
        response = test_client.get("/openapi.json")
        assert response.status_code == 200

        schema = response.json()
        assert "openapi" in schema
        assert "info" in schema
        assert schema["info"]["title"] == "Users API"

    def test_swagger_ui(self, test_client: TestClient):
        """Test that Swagger UI is accessible."""
        response = test_client.get("/docs")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

    def test_redoc(self, test_client: TestClient):
        """Test that ReDoc is accessible."""
        response = test_client.get("/redoc")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]


# Pytest configuration for running specific test classes
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
