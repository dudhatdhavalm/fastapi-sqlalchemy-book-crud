#
#import pytest
#from app import app, crud
#from app.tests.utils.authors import create_random_author
#from app.tests.utils.books import create_random_book
#from app.api.dependencies import get_db
#from fastapi.testclient import TestClient
#from app.api.endpoints.book import *
#from app.schemas.book import BookCreate, BookUpdate
#from app.models.author import Author
#from typing import Any, Dict
#
#
#from app import app
#from sqlalchemy.orm import Session
#
#client = TestClient(app)
#
#
#def test_valid_book_update(db: Session) -> None:
#    """
#    This test checks the happy path scenario of updating a book.
#    It starts by creating a new book using some random data.
#    Then, new data for the book is defined and the update_book endpoint is called.
#    Finally the assertions are done to check if the update was successful
#    """
#    # Create a random book
#    book = create_random_book(db)
#    # Create a random author
#    author = create_random_author(db)
#
#    # Define new data for the book
#    book_data = {"title": "New Title", "author_id": author.id}
#
#    book_in_update = BookUpdate(**book_data)
#    response = client.put(f"/books/{book.id}", json=book_in_update.dict())
#
#    assert response.status_code == 200
#    updated_book = response.json()
#    assert updated_book["title"] == book_data["title"]
#    assert updated_book["author_id"] == book_data["author_id"]
#
#    # cleanup
#    crud.book.remove(db, id=book.id)
#
#
#def test_invalid_author_book_update(db: Session) -> None:
#    """
#    This test checks the scenario where we are updating a book,
#    but the author_id provided does not exist in the database.
#    It starts by creating a new book using some random data.
#    Then, new data for the book is defined with a non-existing author id and the update_book endpoint is called.
#    Finally the assertions are done to check if the correct HTTP status code and error message is returned
#    """
#    # Create a random book
#    book = create_random_book(db)
#
#    # Define new data for the book with a non-existing author id
#    book_data = {"title": "New Title", "author_id": 999999}
#
#    book_in_update = BookUpdate(**book_data)
#    response = client.put(f"/books/{book.id}", json=book_in_update.dict())
#
#    assert response.status_code == 404
#    assert response.json()["detail"] == f"Author id {book_data['author_id']} not found"
#
#    # cleanup
#    crud.book.remove(db, id=book.id)
#
#
#def test_non_existent_book_update(db: Session) -> None:
#    """
#    This test checks the scenario where we are trying to update a book that does not exist.
#    The update_book endpoint is called with a non-existing book id.
#    Finally the assertions are done to check if the correct HTTP status code and error message is returned
#    """
#    # Define new data for the book
#    book_data = {"title": "New Title", "author_id": 1}
#
#    book_in_update = BookUpdate(**book_data)
#    response = client.put(f"/books/999999", json=book_in_update.dict())
#
#    assert response.status_code == 404
#    assert response.json()["detail"] == "Book id 999999 not found"
#