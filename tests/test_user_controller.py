import os
import sys
import pytest

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
