import os
import sys
import pytest

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

from main import app
from fastapi.testclient import TestClient
from models.users import User, UserSchemaBase
from database.db import get_db

client = TestClient(app)


# Function that returns an instance of a database session
@pytest.fixture
def db_session():
    return next(get_db())


# Function to clear the data in the User table
@pytest.fixture
def clear_tables(db_session):
    db_session.query(User).delete()
    db_session.commit()


# Function that returns a sample of the user_data
@pytest.fixture
def sample_user_data():
    return {"username": "test_user"}


# Validate the endpoint for creating a user
def test_create_user_endpoint(clear_tables, sample_user_data):
    # Send a POST request to the /users endpoint passing in the sample user data
    response = client.post("/users", json=sample_user_data)
    assert response.status_code == 200

    # Validate that the username of the returned user equals the username in the payload
    data = response.json()
    assert "username" in data
    assert data["username"] == sample_user_data["username"]
