#
#from app.api.endpoints.book import *
#
#
#from unittest.mock import MagicMock
#from fastapi import HTTPException, status
#
#import pytest
#import pytest
#from sqlalchemy.orm import Session
#
#
#def test_delete_book_no_errors(mock_db_session, mock_crud_remove_success):
#    """
#    Test that the delete_book function executes without throwing errors.
#    """
#    response = delete_book(book_id=1, db=mock_db_session)
#    assert response is not None
#
#
#@pytest.fixture(scope="function")
#def db_session():
#    """
#    Returns a mock database session.
#    """
#    yield MagicMock(spec=Session)
#
#
#@pytest.fixture(scope="function")
#def db_book_exists(db_session):
#    """
#    Pretend that the book exists in the database.
#    """
#    crud.book.remove = MagicMock(return_value=True)
#    return db_session
#
#
#@pytest.fixture(scope="function")
#def db_book_not_found(db_session):
#    """
#    Pretend that the book doesn't exist in the database and raises an HTTPException.
#    """
#    crud.book.remove = MagicMock(
#        side_effect=HTTPException(
#            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
#        )
#    )
#    return db_session
#
#
#def test_delete_existing_book(db_book_exists):
#    """
#    Test deleting a book that exists and makes sure no errors are thrown.
#    """
#    response = delete_book(book_id=1, db=db_book_exists)
#    assert response is not None
#
#
#def test_delete_non_existing_book(db_book_not_found):
#    """
#    Test deleting a book that doesn't exist should throw an HTTP 404 error.
#    """
#    with pytest.raises(HTTPException) as exc_info:
#        delete_book(book_id=999, db=db_book_not_found)
#    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
#
#
#@pytest.fixture(scope="function")
#def mock_db_session():
#    db_session = MagicMock(spec=Session)
#    db_session.close = MagicMock()
#    yield db_session
#    db_session.close.assert_called_once()
#
#
#def test_delete_book_no_errors(mock_db_session, mock_crud_remove_success):
#    response = delete_book(book_id=1, db=mock_db_session)
#    assert response is not None
#
#
#@pytest.fixture(scope="function")
#def db_book_exists(mock_db_session):
#    crud.book.remove = MagicMock(return_value=True)
#    return mock_db_session
#
#
#@pytest.fixture(scope="function")
#def db_book_not_found(mock_db_session):
#    crud.book.remove = MagicMock(
#        side_effect=HTTPException(
#            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
#        )
#    )
#    return mock_db_session
#
#
#def test_delete_existing_book(db_book_exists):
#    response = delete_book(book_id=1, db=db_book_exists)
#    assert response is not None
#
#
#def test_delete_non_existing_book(db_book_not_found):
#    with pytest.raises(HTTPException) as exc_info:
#        delete_book(book_id=999, db=db_book_not_found)
#    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
#