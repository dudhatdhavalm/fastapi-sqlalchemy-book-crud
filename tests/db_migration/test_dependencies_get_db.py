#from app.main import app
#from app.api.dependencies import *
#import pytest
#from starlette.testclient import TestClient
#from sqlalchemy.orm import Session
#
#
#@pytest.fixture(scope="module")
#def client():
#    with TestClient(app) as test_client:
#        yield test_client
#
#
#@pytest.fixture(scope="module")
#def db():
#    try:
#        db = get_db()
#        return next(db)
#    finally:
#        db.close()
#
#
#def test_get_db_exists():
#    """Test if the `get_db` function exists."""
#    assert "get_db" in globals(), f"The function `get_db` does not exist."
#
#
#def test_get_db_no_error():
#    """
#    Tests if the function `get_db` throws no error
#    when it is executed
#    """
#    try:
#        get_db()
#    except Exception as e:
#        pytest.fail(f"`get_db()` raised exception {type(e).__name__}: {e}")
#
#
#def test_get_db_return_type():
#    """Test the return type of the `get_db` function."""
#    db = get_db()
#    assert isinstance(
#        db, Session
#    ), f"`get_db()` should return an instance of `Session`, got {type(db).__name__}"
#
#
#def test_get_db_not_none():
#    """
#    Tests if the function `get_db` returns a
#    non-None value when it is executed.
#    """
#    assert get_db() is not None, "The returning value of `get_db()` was None."
#