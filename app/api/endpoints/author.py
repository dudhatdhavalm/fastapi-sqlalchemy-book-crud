from fastapi import APIRouter, Depends, HTTPException, Request
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
def create_author(
    *, author_in: AuthorCreate, db: Session = Depends(dependencies.get_db)
):
    author = crud.author_plain.create(db=db, obj_in=author_in)
    return author


@router.get("", status_code=200)
def get_author(*, db: Session = Depends(dependencies.get_db)):
    author = crud.author_plain.get(db=db)
    return author


@router.get("/{author_id}", status_code=200)
def get_by_id(*, author_id: int, db: Session = Depends(dependencies.get_db)):
    author = crud.author_plain.get_by_author_id(db=db, id=author_id)

    if author is None:
        raise HTTPException(status_code=404, detail=f"Author id {author_id} not found")

    return author


@router.put("/{author_id}", status_code=200)
def update_author(
    *,
    author_id: int,
    author_in: AuthorUpdate,
    db: Session = Depends(dependencies.get_db),
):
    result = crud.author_plain.get_by_author_id(db=db, id=author_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Author id {author_id} not found")
    
    author = crud.author_plain.update(db=db, db_obj=result, obj_in=author_in)
    return author

@router.delete("/{author_id}",status_code=200)
def delete_author(*, author_id: int, db: Session = Depends(dependencies.get_db)) -> dict:
    """
    Delete Author
    """
    result = crud.author.remove(db=db, id=author_id)
    return {"detail": f"Author id {author_id} deleted successfully"}