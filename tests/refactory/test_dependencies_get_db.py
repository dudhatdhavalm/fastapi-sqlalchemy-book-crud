

import app.db.database
from app.api.dependencies import *
from sqlalchemy.orm import Session
import get_db
from sqlalchemy.exc import OperationalError
import pytest


def test_get_db(mocker):
    # Mock the SessionLocal and close functions.
    mocker.patch(
        "app.db.database.SessionLocal", return_value=mocker.MagicMock(spec=Session)
    )
    mock_close = mocker.patch("app.db.database.SessionLocal.close")

    # Call the get_db function
    db_gen = get_db()
    db = next(db_gen)

    # Check if the mocked SessionLocal was called
    app.db.database.SessionLocal.assert_called_once()
    # The close function shouldn't be called until we exhaust the generator
    mock_close.assert_not_called()

    # Raise StopIteration by calling next again to trigger the finally block
    with pytest.raises(StopIteration):
        next(db_gen)

    # Now the close function should have been called once
    mock_close.assert_called_once()


def test_get_db_exception(mocker):
    # Mock the SessionLocal to raise an exception
    mocker.patch("app.db.database.SessionLocal", side_effect=OperationalError)

    # Call the get_db function and check if it raises an exception
    with pytest.raises(OperationalError):
        db_gen = get_db()
        next(db_gen)
