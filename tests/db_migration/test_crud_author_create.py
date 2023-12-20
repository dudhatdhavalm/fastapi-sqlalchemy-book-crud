#from sqlalchemy import create_engine
#from app.schemas.author import AuthorCreate
#from app.models.author import Author
#from sqlalchemy.orm import Session, sessionmaker
#from app.crud.crud_author import CRUDAuthor
#import pytest
#from app.crud.crud_author import *
#
#
## setup database connection
#@pytest.fixture(scope="module")
#def db():
#    DATABASE_URL = "postgresql://root:postgres@localhost/code_robotics_1701690361803"
#    engine = create_engine(DATABASE_URL)
#    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#    return SessionLocal()
#
#
#def test_create(db: Session):
#    # Setup
#    crud_author = CRUDAuthor(Author)
#    author_create = AuthorCreate(name="Test Author")
#
#    # Execute
#    result = crud_author.create(db, obj_in=author_create)
#
#    # Validate
#    assert result is not None
#    assert isinstance(result, Author)
#
#
#def test_create_no_name(db: Session):
#    # Setup
#    crud_author = CRUDAuthor(Author)
#    author_create = AuthorCreate(name="")
#
#    # Execute
#    with pytest.raises(ValueError):
#        result = crud_author.create(db, obj_in=author_create)
#
#
#def test_create_with_non_unicode(db: Session):
#    # Setup
#    crud_author = CRUDAuthor(Author)
#    author_create = AuthorCreate(name="Author\x00Name")
#
#    # Execute
#    result = crud_author.create(db, obj_in=author_create)
#
#    # Validate
#    assert result is not None
#    assert result.name == "AuthorName"
#