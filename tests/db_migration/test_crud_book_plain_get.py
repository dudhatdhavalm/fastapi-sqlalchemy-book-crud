#from app.db.base_class import Base
#from sqlalchemy import create_engine
#from app.crud.crud_book_plain import *
#from app.models.book import Book
#from sqlalchemy.orm import Session, sessionmaker
#
#
#import pytest
#import pytest
#
#engine = create_engine(
#    "postgresql://username:password@localhost/code_robotics_1701690361803"
#)
#
#
#engine = create_engine(
#    "postgresql://postgres:pg123@localhost/code_robotics_1701690361803"
#)
#
#engine = create_engine(
#    "postgresql://root:postgres@localhost/code_robotics_1701690361803"
#)
#SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
#
#def setup_module(module):
#    Base.metadata.create_all(bind=engine)
#
#
#def teardown_module(module):
#    Base.metadata.drop_all(bind=engine)
#
#
#@pytest.fixture
#def db() -> Session:
#    db = SessionLocal()
#    try:
#        yield db
#    except Exception:
#        db.rollback()
#    finally:
#        db.close()
#
#
#def test_get_valid(db: Session):
#    from app.crud.crud_book_plain import CRUDBook
#
#    crud_book = CRUDBook()
#    result = crud_book.get(db)
#    assert result is not None
#
#
#def test_get_zero_limit(db: Session):
#    from app.crud.crud_book_plain import CRUDBook
#
#    crud_book = CRUDBook()
#    result = crud_book.get(db, limit=0)
#    assert len(result) == 0
#
#
#def test_get_skip(db: Session):
#    from app.crud.crud_book_plain import CRUDBook
#
#    crud_book = CRUDBook()
#    result = crud_book.get(db, skip=2)
#    assert len(result) <= 98
#