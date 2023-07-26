import os
import sys
import pytest

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

from main import app
from fastapi.testclient import TestClient
from models.users import User, UserSchemaBase


# Function that returns an instance of a database session
@pytest.fixture
def db_session():
    return next(get_db())


# Function to clear the data in the User table
@pytest.fixture
def clear_tables(db_session):
    db_session.query(User).delete()
    db_session.commit()
