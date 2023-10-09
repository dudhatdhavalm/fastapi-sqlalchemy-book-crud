from app.crud.crud_book import *

from app.models.book import Book


from typing import List
from sqlalchemy.orm import Session
from pytest import fixture
import pytest


def test_get_multi(
    records: List[Book], db: Session, skip: int = 0, limit: int = 3
) -> None:
    """
    Test 'get_multi' method from 'CRUDBook' class

    Given a list of Book records and parameters `skip` and `limit`,
    this test ensures that 'get_multi' returns the correct slice of records from the database
    when 'skip' is provided and 'limit' is less than the total number of records.

    Args:
        records (List[Book]): a list of Book records.
        db (Session): database session.
        skip (int, optional): the number of records to skip in a query.
        limit (int, optional): the maximum number of records to return in a query.
    """

    class CRUDBook_:
        get_multi = CRUDBook.get_multi

    # Assume that 'records' holds all entries in the 'Book' table (in sorted order)
    expected_records = records[skip : skip + limit]

    # Call 'get_multi' and compare the result with the expected slice of records
    assert CRUDBook_.get_multi(db, skip=skip, limit=limit) == expected_records
