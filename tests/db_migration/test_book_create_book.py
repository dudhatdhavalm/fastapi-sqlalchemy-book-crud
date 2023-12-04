#from datetime import datetime
#
#import pytest
#from fastapi import HTTPException, status
#from fastapi.testclient import TestClient
#from sqlalchemy.orm import Session
#
#
#from datetime import datetime
#from app.tests.utils.utils import random_lower_string
#from app.core.config import settings
#
#from app import crud
#from app.api.endpoints.book import *
#from app import crud
#from app.main import app
#from app.models.author import Author
#from starlette.datastructures import Secret
#from app.schemas.book import BookCreate
#
#
#def test_get_book_no_errors(db: Session) -> None:
#    response = app.client.get("/api/books/")
#    assert response
#    assert response.status_code == 200
#
#
#def test_get_book_author_exists(db: Session) -> None:
#    book_name = random_lower_string()
#    book_summary = random_lower_string()
#    book_genre = random_lower_string()
#    book_rating = 5
#    book_year_of_publication = "2021"
#
#    author = Author(
#        name=random_lower_string(), email=random_lower_string() + "@test.com"
#    )
#    db.add(author)
#    db.commit()
#    db.refresh(author)
#
#    book_in = BookCreate(
#        title=book_name,
#        author_id=author.uuid,
#        summary=book_summary,
#        genre=book_genre,
#        rating=book_rating,
#        year_of_publication=book_year_of_publication,
#    )
#
#    response = app.client.post("/api/books/", data=book_in.json())
#
#    assert response.status_code == 200
#    assert response.json()["name"] == book_name
#    assert response.json()["summary"] == book_summary
#    assert response.json()["author_uuid"] == str(author.uuid)
#    assert response.json()["year_of_publication"] == book_year_of_publication
#    assert response.json()["rating"] == book_rating
#    assert response.json()["genre"] == book_genre
#
#
#def test_get_book_author_not_found(db: Session) -> None:
#    book_name = random_lower_string()
#    book_summary = random_lower_string()
#    book_rating = 5
#    book_year_of_publication = "2021"
#    book_genre = random_lower_string()
#    book_in = BookCreate(
#        title=book_name,
#        author_id=-1,
#        summary=book_summary,
#        genre=book_genre,
#        rating=book_rating,
#        year_of_publication=book_year_of_publication,
#    )
#    response = app.client.post("/api/books/", data=book_in.json())
#    assert response.status_code == 404
#    assert response.json() == {"detail": f"Author id {book_in.author_id} not found"}
#