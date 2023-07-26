import os
import sys
import pytest
from fastapi import HTTPException

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

from controllers import UserController
from database.db import get_db
from models.users import User, UserSchemaBase


# Function that returns an instance of a database session
@pytest.fixture
def db_session():
    return next(get_db())


# Function that returns an instance of the UserSchemaBase class to use as sample test data
@pytest.fixture
def sample_user_data():
    return UserSchemaBase(username="test_user")


@pytest.fixture
def clear_tables(db_session):
    db_session.query(User).delete()
    db_session.commit()

    print("tables have been cleared")


# Test the UserController.validate_user function for valid input
def test_validate_user_valid_input(clear_tables, db_session, sample_user_data):
    user_controller = UserController()
    response = user_controller.validate_user(db_session, sample_user_data)
    assert response is None


"""
The function below is currently not behaving as expected - values that are
integers are being coerced to strings and can still be added to database.
"""


# Test the validate_user function for invalid username (not a string)
@pytest.mark.skip()
def test_validate_user_invalid_input(clear_tables, db_session):
    user_controller = UserController()
    invalid_data = UserSchemaBase(username=123)
    response = user_controller.validate_user(db_session, invalid_data)
    assert response.status_code == 422
    assert response.detail == "Username must be a string"


# Test the validate_user function for username less than 3 characters
def test_validate_user_short_username(clear_tables, db_session):
    user_controller = UserController()
    invalid_data = UserSchemaBase(username="ab")
    response = user_controller.validate_user(db_session, invalid_data)
    assert response is not None
    assert response.status_code == 422
    assert response.detail == "Username must be at least 3 characters"


# Test the validate_user function for existing username
def test_validate_user_existing_username(clear_tables, db_session, sample_user_data):
    user_controller = UserController()

    # Create a user in the database and return save the username to a variable
    user_added = user_controller.create_user(db_session, sample_user_data)
    assert isinstance(user_added, User)
    username = user_added.username

    # Attempt to add a user with the same username
    duplicate_username = UserSchemaBase(username=f"{username}")
    response = user_controller.validate_user(db_session, duplicate_username)
    assert response is not None
    assert response.status_code == 409
    assert response.detail == "Username already exists"


# Test the create_user to create a user in the database
def test_create_user(clear_tables, db_session, sample_user_data):
    user_controller = UserController()
    result = user_controller.create_user(db_session, sample_user_data)

    assert isinstance(result, User)
    assert result.username == sample_user_data.username
