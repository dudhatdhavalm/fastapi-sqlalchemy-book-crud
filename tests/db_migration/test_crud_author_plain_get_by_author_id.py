#import pytest
#
#from app.crud.crud_author_plain import *
#
#
## Test if function doesn't throw errors when it's executed
#def test_get_by_author_id_no_errors(db: Session, sample_author: Author):
#    crud_author = CRUDAuthor()
#    try:
#        crud_author.get_by_author_id(db, sample_author.id)
#    except Exception as e:
#        pytest.fail(f"Unexpected error occurred: {e}")
#
#
## Test if function returns an object when given valid id
#def test_get_by_author_id_returns_object(db: Session, sample_author: Author):
#    crud_author = CRUDAuthor()
#    result = crud_author.get_by_author_id(db, sample_author.id)
#    # We don't check for specific value, just for object type
#    assert isinstance(result, Author)
#
#
## Test if function returns None when given invalid id
#def test_get_by_author_id_invalid_id(db: Session):
#    crud_author = CRUDAuthor()
#    result = crud_author.get_by_author_id(
#        db, 999
#    )  # Most likely an id that doesn't exist in the database
#    assert result is None
#