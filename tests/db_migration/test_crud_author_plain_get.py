#from app.models.author import Author
#from sqlalchemy import create_engine
#from app.crud.crud_author_plain import CRUDAuthor
#from typing import List
#
#from app.crud.crud_author_plain import *
#
#import pytest
#from sqlalchemy.orm import Session as SessionType
#from sqlalchemy.orm import sessionmaker
#
## Create an engine that stores data in the memory
#engine = create_engine("sqlite:///:memory:", echo=True)
#
## Create a configured "Session" class
#Session = sessionmaker(bind=engine)
#
## Create a Session
#session = Session()
#
#
#@pytest.fixture(scope="module")
#def db() -> SessionType:
#    return session
#
#
#@pytest.fixture(scope="module")
#def crud_author():
#    return CRUDAuthor()
#
#
#@pytest.fixture(scope="module")
#def author_data(db: Session):
#    # Create objects
#    author1 = Author(id=1, name="Author1")
#    author2 = Author(id=2, name="Author2")
#
#    db.add(author1)
#    db.add(author2)
#
#    db.commit()
#
#    return [author1, author2]
#
#
#def test_get(crud_author: CRUDAuthor, db: Session, author_data: List[Author]):
#    result = crud_author.get(db)
#    assert result is not None
#    assert isinstance(result, list)
#
#
#def test_get_with_skip_limit(
#    crud_author: CRUDAuthor, db: Session, author_data: List[Author]
#):
#    result = crud_author.get(db, skip=1, limit=1)
#    assert result is not None
#    assert isinstance(result, list)
#