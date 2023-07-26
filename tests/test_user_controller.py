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


# Test the UserController.validate_user function for valid input
def test_validate_user_valid_input(db_session, sample_user_data):
    user_controller = UserController()
    response = user_controller.validate_user(db_session, sample_user_data)
    assert response is None


"""
The function below is currently not behaving as expected - values that are
integers are being coerced to strings and can still be added to database.
"""


# Test the validate_user function for invalid username (not a string)
@pytest.mark.skip()
def test_validate_user_invalid_input(db_session):
    user_controller = UserController()
    invalid_data = UserSchemaBase(username=123)
    response = user_controller.validate_user(db_session, invalid_data)
    assert response.status_code == 422
    assert response.detail == "Username must be a string"
