#from sqlalchemy.orm import Session, sessionmaker
#from sqlalchemy import create_engine
#from typing import Dict
#from app.crud.crud_author_plain import *
#from app.models.author import Author
#
#from app.crud.crud_author import CRUDAuthor
#
#import pytest
#
#engine = create_engine("postgresql://postgres:root@host.docker.internal:5432/")
#SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
#
#@pytest.fixture
#def setup_db() -> Session:
#    return SessionLocal()
#
#
#@pytest.fixture
#def setup_author_model(setup_db: Session) -> Author:
#    author = Author(name="Test Author")
#    setup_db.add(author)
#    setup_db.commit()
#    setup_db.refresh(author)
#    return author
#
#
#@pytest.fixture
#def setup_crud_author() -> CRUDAuthor:
#    return CRUDAuthor()
#
#
#def test_update(
#    setup_author_model: Author,
#    setup_db: Session,
#    setup_crud_author: CRUDAuthor,
#) -> None:
#    update_data = {"name": "Updated Author"}
#    updated_author = setup_crud_author.update(
#        db=setup_db, db_obj=setup_author_model, obj_in=update_data
#    )
#    assert updated_author is not None
#    assert updated_author.name == "Updated Author"
#
#
#def test_update_with_no_changes(
#    setup_author_model: Author,
#    setup_db: Session,
#    setup_crud_author: CRUDAuthor,
#) -> None:
#    updated_author = setup_crud_author.update(
#        db=setup_db, db_obj=setup_author_model, obj_in=setup_author_model
#    )
#    assert updated_author is not None
#    assert updated_author.name == setup_author_model.name
#