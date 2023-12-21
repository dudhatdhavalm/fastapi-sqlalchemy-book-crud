from app.schemas.author import AuthorCreate
from app.models.author import Author

import pytest
from unittest.mock import Mock

from app.crud.crud_author_plain import *
from datetime import date
from sqlalchemy.orm import Session


# Fixtures and sample data
@pytest.fixture
def db_session() -> Session:
    """Fixture for creating a mock database session."""
    return Mock(spec=Session)


@pytest.fixture
def author_create_data() -> AuthorCreate:
    """Fixture for generating AuthorCreate sample data."""
    return AuthorCreate(name="Jane Doe", birth_date=date(1985, 5, 23))


@pytest.fixture
def author_instance() -> Author:
    """Fixture for generating Author sample data."""
    author = Mock(spec=Author)
    author.id = 1
    author.name = "Jane Doe"
    author.birth_date = date(1985, 5, 23)
    return author


# Tests
def test_create_no_exceptions(
    db_session: Session, author_create_data: AuthorCreate, author_instance: Author
):
    """Test that the create function doesn't throw exceptions."""
    crud_author = CRUDAuthor()
    db_session.add = Mock()
    db_session.commit = Mock()
    db_session.refresh = Mock(return_value=author_instance)

    result = crud_author.create(db=db_session, obj_in=author_create_data)
    assert result is not None


def test_create_return_value(
    db_session: Session, author_create_data: AuthorCreate, author_instance: Author
):
    """Test that the create function returns an Author instance."""
    crud_author = CRUDAuthor()
    db_session.add = Mock()
    db_session.commit = Mock()
    db_session.refresh = Mock(return_value=author_instance)

    result = crud_author.create(db=db_session, obj_in=author_create_data)
    assert isinstance(result, Author)


def test_create_persists_object(db_session: Session, author_create_data: AuthorCreate):
    """Test that the create function successfully persists an object."""
    crud_author = CRUDAuthor()
    db_session.add = Mock()
    db_session.commit = Mock()
    db_session.refresh = Mock()

    crud_author.create(db=db_session, obj_in=author_create_data)

    db_session.add.assert_called_once()
    db_session.commit.assert_called_once()
    db_session.refresh.assert_called_once()


# Standard library imports
from unittest.mock import Mock

# Pytest import
import pytest

# Local application imports
from app.models.author import Author
