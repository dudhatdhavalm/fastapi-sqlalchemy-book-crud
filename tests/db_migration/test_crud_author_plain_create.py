#
#import pytest
#from app.crud.crud_author_plain import CRUDAuthor
#from app.schemas.author import AuthorCreate
#from app.models.author import Author
#from typing import Any, Dict, List, Union
#from app.crud.crud_author_plain import *
#from sqlalchemy.orm import Session
#
#
#@pytest.fixture
#def db_session() -> Session:
#    return Session()
#
#
#@pytest.fixture
#def author_create() -> AuthorCreate:
#    return AuthorCreate(
#        name="Test_name", date_of_birth="1989-01-25", nationality="Fictional"
#    )
#
#
#@pytest.fixture
#def prepared_author(db_session: Session, author_create: AuthorCreate) -> Author:
#    crud_author = CRUDAuthor()
#    return crud_author.create(db_session, obj_in=author_create)
#
#
#def test_create(prepared_author: Author) -> None:
#    assert prepared_author is not None
#    assert isinstance(prepared_author, Author)
#    assert prepared_author.name == "Test_name"
#    assert prepared_author.date_of_birth == "1989-01-25"
#    assert prepared_author.nationality == "Fictional"
#