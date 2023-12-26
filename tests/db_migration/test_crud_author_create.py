
from app.models.author import Author

import pytest
from unittest.mock import create_autospec

from app.crud.crud_author import *
from app.schemas.author import AuthorCreate
from app.models.author import Author
from sqlalchemy.orm import Session

# Assuming CRUDAuthor class is properly imported within the test file's context
# from app.crud.crud_author import CRUDAuthor


@pytest.fixture
def mock_db_session():
    """Provide a mock SQLAlchemy Session object."""
    return create_autospec(Session, instance=True)


@pytest.fixture
def author_create_data():
    """Provide a mock AuthorCreate schema object."""
    return AuthorCreate(name="Test Author", email="test@example.com")


@pytest.fixture
def crud_author(mock_db_session):
    """Provide a CRUDAuthor instance with a mocked model attribute."""
    crud_author_instance = CRUDAuthor(model=Author)
    crud_author_instance.model = (
        Author  # Mock the model attribute, if it is not attribute of CRUDAuthor
    )
    return crud_author_instance


def test_create_no_errors(crud_author, mock_db_session, author_create_data):
    """Test that the `create` function does not throw any errors during execution."""
    try:
        author = crud_author.create(db=mock_db_session, obj_in=author_create_data)
        assert author is not None, "The create method should return a non-None value."
    except Exception as exc:
        pytest.fail(f"An exception occurred: {exc}")


def test_create_db_add_called(crud_author, mock_db_session, author_create_data):
    """Test that the `create` method calls 'add' on the database session."""
    crud_author.create(db=mock_db_session, obj_in=author_create_data)
    mock_db_session.add.assert_called_once()


def test_create_db_commit_called(crud_author, mock_db_session, author_create_data):
    """Test that the `create` method calls 'commit' on the database session."""
    crud_author.create(db=mock_db_session, obj_in=author_create_data)
    mock_db_session.commit.assert_called_once()


def test_create_db_refresh_called(crud_author, mock_db_session, author_create_data):
    """Test that the `create` method calls 'refresh' on the database session."""
    crud_author.create(db=mock_db_session, obj_in=author_create_data)
    mock_db_session.refresh.assert_called_once()


def test_create_with_none_data_raises_error(crud_author, mock_db_session):
    """Test that providing None as `obj_in` raises the appropriate error."""
    with pytest.raises(Exception):
        crud_author.create(db=mock_db_session, obj_in=None)


def test_create_with_invalid_data_type_raises_error(crud_author, mock_db_session):
    """Test that providing an invalid type for `obj_in` raises the appropriate error."""
    with pytest.raises(Exception):
        invalid_data = "not an AuthorCreate instance"
        crud_author.create(db=mock_db_session, obj_in=invalid_data)


# Since we are using classes (`Author`, `AuthorCreate`) from app.models.author, app.schemas.author,
# and `Session` from sqlalchemy.orm, they need not to be imported again as per guidelines.


from unittest.mock import create_autospec
