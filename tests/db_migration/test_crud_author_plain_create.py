#
#
#from datetime import date
#from sqlalchemy import create_engine
#
#import pytest
#from sqlalchemy.orm import sessionmaker
#
#from app.crud.crud_author_plain import *
#import pytest
#
#
#@pytest.fixture(scope="module")
#def db() -> Session:
#    """Yields a SQLAlchemy session and ensures it is closed after use."""
#    engine = create_engine(DATABASE_URL)
#    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#    connection = engine.connect()
#    transaction = connection.begin()
#    session = SessionLocal(bind=connection)
#    yield session
#    session.close()
#    transaction.rollback()
#    connection.close()
#
#
#@pytest.fixture(scope="module")
#def author_create_data() -> AuthorCreate:
#    """Provides AuthorCreate schema sample data."""
#    return AuthorCreate(first_name="John", last_name="Doe", birth_date=date(1990, 1, 1))
#
#
#@pytest.fixture(scope="module")
#def crud_author() -> CRUDAuthor:
#    """Provides an instance of CRUDAuthor."""
#    return CRUDAuthor()
#
#
#def test_create_author_no_error(
#    db: Session, author_create_data: AuthorCreate, crud_author: CRUDAuthor
#):
#    """Test to ensure the create function does not throw errors when called."""
#    assert crud_author.create(db=db, obj_in=author_create_data) is not None
#
#
#def test_create_author_correct_instance(
#    db: Session, author_create_data: AuthorCreate, crud_author: CRUDAuthor
#):
#    """Test to check if the returned object is an instance of Author."""
#    result = crud_author.create(db=db, obj_in=author_create_data)
#    assert isinstance(result, Author)
#
#
#def test_create_author_correct_data(
#    db: Session, author_create_data: AuthorCreate, crud_author: CRUDAuthor
#):
#    """Test to verify that the created author has correct data."""
#    result = crud_author.create(db=db, obj_in=author_create_data)
#    assert result.first_name == author_create_data.first_name
#    assert result.last_name == author_create_data.last_name
#    assert result.birth_date == author_create_data.birth_date
#