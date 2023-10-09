import app.db.database
from app.api.dependencies import *
from sqlalchemy.orm import Session
import get_db
from sqlalchemy.exc import OperationalError
import pytest
import pymongo
from pymongo import MongoClient
from pymongo.errors import OperationFailure





def test_get_db_exception(mocker):
    # Mock the MongoClient to raise an exception
    mocker.patch("pymongo.MongoClient", side_effect=OperationFailure)

    # Call the get_db function and check if it raises an exception
    with pytest.raises(OperationFailure):
        db_gen = get_db()
        next(db_gen)


def test_get_db(mocker):
    # Mock the MongoClient and close functions.
    mocker.patch(
        "pymongo.MongoClient", return_value=mocker.MagicMock(spec=MongoClient)
    )
    mock_close = mocker.patch("pymongo.MongoClient.close")

    # Call the get_db function
    db_gen = get_db()
    db = next(db_gen)

    # Check if the mocked MongoClient was called
    pymongo.MongoClient.assert_called_once()
    # The close function shouldn't be called until we exhaust the generator
    mock_close.assert_not_called()

    # Raise StopIteration by calling next again to trigger the finally block
    with pytest.raises(StopIteration):
        next(db_gen)

    # Now the close function should have been called once
    mock_close.assert_called_once()
