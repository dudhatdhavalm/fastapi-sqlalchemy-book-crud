#from app.models.author import Author
#from datetime import date
#from sqlalchemy.orm import Session, sessionmaker
#from sqlalchemy import create_engine
#from app.crud.crud_author_plain import CRUDAuthor
#from app.schemas.author import AuthorCreate
#
#from app.crud.crud_author_plain import *
#
#import pytest
#
#from app.crud.crud_author_plain import CRUDAuthor
#
#
#from datetime import date
#
#
## Define necessary fixtures and sample data for the test
#@pytest.fixture
#def sample_author_create_obj() -> AuthorCreate:
#    return AuthorCreate(
#        name="Test Author",
#        title="Test Title",
#        description="Test Description",
#        dob=date.today(),
#    )
#
#
#@pytest.fixture
#def db() -> Session:
#    SQLALCHEMY_DATABASE_URL = "postgresql://postgres:root@host.docker.internal:5432/"
#    engine = create_engine(SQLALCHEMY_DATABASE_URL)
#    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#    with TestingSessionLocal() as db:
#        yield db
#
#
## Tests
#def test_create_author_not_none(db: Session, sample_author_create_obj: AuthorCreate):
#    """Test to check if the create method doesn't throw errors when it's executed."""
#    crud_author = CRUDAuthor()
#    author_result = crud_author.create(db=db, obj_in=sample_author_create_obj)
#    assert author_result is not None
#
#
#def test_create_author_type(db: Session, sample_author_create_obj: AuthorCreate):
#    """Test to check if the create method returns an instance of Author."""
#    crud_author = CRUDAuthor()
#    author_result = crud_author.create(db=db, obj_in=sample_author_create_obj)
#    assert isinstance(author_result, Author)
#
#
#def test_create_author_data(db: Session, sample_author_create_obj: AuthorCreate):
#    """Test to check if the create method returns the correct data with legitimate properties."""
#    crud_author = CRUDAuthor()
#    author_result = crud_author.create(db=db, obj_in=sample_author_create_obj)
#    assert author_result.name == sample_author_create_obj.name
#    assert author_result.title == sample_author_create_obj.title
#    assert author_result.description == sample_author_create_obj.description
#    assert author_result.dob == sample_author_create_obj.dob
#