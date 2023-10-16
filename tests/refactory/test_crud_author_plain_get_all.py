import pytest
from sqlalchemy import Column, Integer, Sequence, String, create_engine
from sqlalchemy.orm import Session, sessionmaker
from app.models.author import Author


import pytest
from sqlalchemy.ext.declarative import declarative_base
from app.crud.crud_author_plain import *

Base = declarative_base()


class TestAuthor(Base):
    __tablename__ = "authors"

    id = Column(Integer, Sequence("author_id_seq"), primary_key=True)
    name = Column(String(50), nullable=False)

    def __init__(self, name):
        self.name = name


@pytest.fixture(scope="module")
def db() -> Session:
    engine = create_engine("postgresql://postgres:root@localhost:5432/")
    connection = engine.connect()

    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    return session


def test_get_all(db: Session):
    crud_author = CRUDAuthor()

    # Mock data
    test_authors = [TestAuthor(name=f"Author {i}") for i in range(10)]
    db.bulk_save_objects(test_authors)
    db.commit()

    authors = crud_author.get_all(db)
    assert authors is not None
    assert len(authors) >= 1

    # Cleanup
    for author in test_authors:
        db.delete(author)

    db.commit()
