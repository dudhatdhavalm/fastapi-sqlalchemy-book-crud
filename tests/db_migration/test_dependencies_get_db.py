#
#import pytest
#
#
#from unittest.mock import patch
#
#from app.api.dependencies import *
#from unittest.mock import patch
#from sqlalchemy.orm import Session
#
#
## Test to ensure the get_db function does not throw errors when executed
#def test_get_db_execution():
#    db_gen = get_db()
#    db = next(db_gen)
#    assert db is not None
#
#
#@pytest.fixture()
#def session_mock():
#    with patch("app.db.database.SessionLocal") as mock:
#        mock.return_value = Session()  # or any other object that can be closed
#        yield mock
#
#
## Test to ensure that db.close is called on database session
#def test_get_db_session_close_call(session_mock):
#    db_gen = get_db()
#    db = next(db_gen)
#    try:
#        next(db_gen)
#    except StopIteration:
#        pass
#    assert session_mock.return_value.close.called
#
#
## Test to ensure that a new database session is created each time
#def test_get_db_creates_new_session_each_time(session_mock):
#    first_db_gen = get_db()
#    second_db_gen = get_db()
#    first_db = next(first_db_gen)
#    second_db = next(second_db_gen)
#    assert first_db is not second_db
#
#
## Test to ensure the db instance is closed after context exits
#def test_get_db_closes_after_context(session_mock):
#    with pytest.raises(StopIteration):
#        db_gen = get_db()
#        db = next(db_gen)
#        next(db_gen)  # should raise StopIteration and close the db
#    assert db.closed
#