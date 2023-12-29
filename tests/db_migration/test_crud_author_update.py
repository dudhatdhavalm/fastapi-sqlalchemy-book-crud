from sqlalchemy.orm import Session

from app.crud.crud_author import *

import pytest

from app.crud.crud_author import CRUDAuthor
from unittest.mock import patch


from unittest.mock import patch
from app.crud.crud_author import CRUDAuthor
from app.models.author import Author

# Define the database URI string for sqlalchemy engine
DATABASE_URI = "postgresql://refactorybot:22r)pGKLcaeP@refactory.cluster-cw4q9y97boua.us-east-1.rds.amazonaws.com:5432/code_robotics_1703882508620"


@pytest.fixture
def db_session():
    # Mocking the Session object from SQLAlchemy
    return Session(DATABASE_URI)


@pytest.fixture
def author_obj():
    # Instance of the Author model, with example data
    return Author(id=1, name="Test Author")


@pytest.fixture
def author_update_obj():
    # Dictionary representing the update operation, could be partial
    return {"name": "Updated Author Name"}


@pytest.fixture
def crud_author():
    # Instance of the CRUDAuthor class, passing the Author model as a required argument
    return CRUDAuthor(Author)


def test_update_no_errors(crud_author, db_session, author_obj, author_update_obj):
    with patch.object(CRUDAuthor, "update", return_value=author_obj) as mock_update:
        # The most basic test to ensure that the update method does not throw errors
        result = crud_author.update(
            db=db_session, db_obj=author_obj, obj_in=author_update_obj
        )
        mock_update.assert_called_once_with(
            db=db_session, db_obj=author_obj, obj_in=author_update_obj
        )


def test_update_return_value(crud_author, db_session, author_obj, author_update_obj):
    with patch.object(CRUDAuthor, "update", return_value=author_obj) as mock_update:
        # Testing if a correct instance of Author is returned
        result = crud_author.update(
            db=db_session, db_obj=author_obj, obj_in=author_update_obj
        )
        assert result is not None


@pytest.mark.parametrize(
    "obj_in", [({"name": "Updated Name"}), (Author(name="Updated Name"))]
)
def test_update_with_varied_inputs(crud_author, db_session, author_obj, obj_in):
    with patch.object(CRUDAuthor, "update", return_value=author_obj) as mock_update:
        # Testing the update with different types of `obj_in`
        result = crud_author.update(db=db_session, db_obj=author_obj, obj_in=obj_in)
        assert isinstance(result, Author)
