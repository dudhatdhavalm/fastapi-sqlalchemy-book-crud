#
#import pytest
#from unittest.mock import patch
#
#from app.api.dependencies import *
#
#
#from typing import Generator
#
#
## Test fixture to provide a database session
#@pytest.fixture(scope="function")
#def db_session():
#    # Mock the actual SessionLocal with a context manager that handles the session's lifecycle
#    with patch("app.db.database.SessionLocal") as mock_SessionLocal:
#        mock_SessionLocal.return_value.close = (
#            lambda: None
#        )  # Mock the close method to do nothing
#        db = mock_SessionLocal()
#        try:
#            yield db
#        finally:
#            db.close()
#
#
## Test if `get_db` does not throw errors and returns a generator
#def test_get_db_no_errors(db_session):
#    db_gen = get_db()
#    db = next(db_gen)
#    assert db is not None
#
#
## Test to ensure that get_db provides a session and can be closed without errors
#def test_get_db_session_close(db_session):
#    with patch("app.db.database.SessionLocal", new=lambda: db_session):
#        db_gen = get_db()
#        db = next(db_gen)
#        db.close()  # should not raise any exceptions
#
#
## Test to ensure get_db function yields a session and then closes it properly
#def test_get_db_yield_session_and_cleanup(db_session):
#    with patch("app.db.database.SessionLocal", new=lambda: db_session):
#        db_gen = get_db()
#        with pytest.raises(StopIteration):
#            next(
#                db_gen
#            )  # This should yield the session and close it, causing a StopIteration
#