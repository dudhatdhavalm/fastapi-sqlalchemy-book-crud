from fastapi import APIRouter, Depends
from app.schemas.author import AuthorCreate
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
