from sqlalchemy.orm import sessionmaker

import pytest
from sqlalchemy import create_engine

from app.models.author import Author
from sqlalchemy.orm.session import Session
from app.crud.crud_author import CRUDAuthor
from app.models.author import Author
from unittest.mock import MagicMock, create_autospec

from app.crud.crud_author import *


from unittest.mock import MagicMock, create_autospec


@pytest.fixture(scope="module")
def test_db_session():
    """Create a test database session."""
    # Setup the connection and the engine
    engine = create_engine(
        "postgresql://refactorybot:22r)pGKLcaeP@refactory.cluster-cw4q9y97boua.us-east-1.rds.amazonaws.com:5432/code_robotics_1704237404964"
    )
    # Session factory bound to the engine
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    # Create a new session
    db_session = SessionLocal()
    return db_session


@pytest.fixture(scope="module")
def author_instance():
    """Create an Author instance."""
    return Author(id=1, name="Test Author")


@pytest.fixture(scope="function")
def mock_db_session():
    """Create a mock SQLAlchemy session object."""
    # Create the mock session and configure methods with `create_autospec`
    mock_session = create_autospec(Session, instance=True)
    return mock_session


@pytest.fixture(scope="function")
def crud_author_instance():
    """Create an instance of CRUDAuthor with mock model."""
    crud_author = CRUDAuthor(model=Author)
    return crud_author


def test_get_by_author_id_no_errors(crud_author_instance, mock_db_session):
    """Test get_by_author_id to check it executes without errors."""
    author_id = 1
    result = crud_author_instance.get_by_author_id(db=mock_db_session, id=author_id)
    assert result is not None


def test_get_by_author_id_invalid_id(crud_author_instance, mock_db_session):
    """Test get_by_author_id with an invalid ID."""
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    invalid_id = 99999
    result = crud_author_instance.get_by_author_id(db=mock_db_session, id=invalid_id)
    assert result is None


def test_get_by_author_id_return_type(
    crud_author_instance, mock_db_session, author_instance
):
    """Test get_by_author_id to ensure it returns an instance of Author when successful."""
    author_id = 1
    mock_db_session.query.return_value.filter.return_value.first.return_value = (
        author_instance
    )
    result = crud_author_instance.get_by_author_id(db=mock_db_session, id=author_id)
    assert isinstance(result, Author)
