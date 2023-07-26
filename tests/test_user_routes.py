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


# Validate the endpoint for getting all users
def test_get_all_users_endpoint(clear_tables, db_session):
    # Add 5 users to the database
    add_users_to_db(db_session, 5)

    # Send a GET request to the /users endpoint
    response = client.get("/users")
    assert response.status_code == 200

    # Test that the number of users created equals all users in the database
    data = response.json()
    assert len(data) == 5


# Helper function to add a n # of unique users to the database
def add_users_to_db(db, num):
    for i in range(num):
        username = f"user{i}"
        new_user = User(username=username)
        db.add(new_user)

    db.commit()
    db.refresh(new_user)
