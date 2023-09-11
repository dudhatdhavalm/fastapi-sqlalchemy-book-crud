from fastapi import APIRouter, Depends, Request
from app.schemas.author import AuthorCreate, AuthorUpdate
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from app.api import dependencies
from app.settings import DATABASE_URL
from app.models.author import Base
from app import crud
engine = create_engine(DATABASE_URL)


def recreate_database():
    Base.metadata.create_all(engine)


recreate_database()

router = APIRouter()


@router.post("", status_code=200)
def create_author(*, author_in: AuthorCreate, db: Session = Depends(dependencies.get_db)):
    author = crud.author.create(db=db, obj_in=author_in)
    return author


@router.get("", status_code=200)
def get_author(*, db: Session = Depends(dependencies.get_db)):
    author = crud.author.get_all(db=db)
    return author


@router.get("/{id}", status_code=200)
def get_by_id(*, author_id: int, db: Session = Depends(dependencies.get_db)):
    author = crud.author.get(db=db, id=author_id)
    return author


@router.put("/{id}", status_code=200)
def update_author(*, request: Request, author_id: int, author_in: AuthorUpdate, db: Session = Depends(dependencies.get_db)):
    result = crud.author.get(db=db, id=author_id)
    author = crud.author.update(db=db, db_obj=result, obj_in=author_in)
    return author
