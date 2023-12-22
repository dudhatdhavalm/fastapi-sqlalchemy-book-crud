
import pytest


from unittest.mock import patch
from unittest.mock import MagicMock, patch

from app.api.dependencies import *
from sqlalchemy.orm import Session

# Pytest code for testing the 'get_db' function
import pytest


# This setup function will create a database URI that is necessary for the mocked database connection
@pytest.fixture(scope="module")
def db_uri():
    db_uri = "postgresql://refactorybot:22r)pGKLcaeP@refactory.cluster-cw4q9y97boua.us-east-1.rds.amazonaws.com:5432/code_robotics_1703260584907"
    return db_uri


# This fixture will mock the database session creation
@pytest.fixture(scope="function")
def mock_session_local(db_uri):
    with patch("app.db.database.SessionLocal") as mock:
        mock.return_value = Session(bind=db_uri)
        yield mock


# Test to check if get_db function doesn't throw errors and yields a database session object
def test_get_db_yields_session(mock_session_local):
    db_generator = get_db()
    db_session = next(db_generator)
    try:
        assert db_session is not None
    finally:
        # Exiting the generator to ensure the database session is closed correctly
        next(db_generator, None)
