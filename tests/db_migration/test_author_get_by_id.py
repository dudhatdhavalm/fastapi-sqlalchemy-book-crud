#from app.crud import author_plain
#from app.api.endpoints.author import *
#
#import pytest
#from fastapi import Depends, HTTPException
#from fastapi.testclient import TestClient
#from app.settings import DATABASE_URL
#from app.models.author import Author
#from app.api import dependencies
#from app.schemas.author import AuthorCreate, AuthorUpdate
#from unittest.mock import Mock
#from sqlalchemy.orm import Session
#
## Create test client instance
#client = TestClient(app)
#
#
#def test_get_by_id_no_error():
#    """Test that get_by_id does not throw errors when called with valid argument"""
#
#    with patch.object(
#        author_plain,
#        "get_by_author_id",
#        return_value=Author(id=1, name="test", email="test@test.com"),
#    ) as mock_method:
#        response = client.get("/author/1")
#        mock_method.assert_called_once_with(db=Session, id=1)
#        assert response.status_code == 200
#        assert response.json() is not None
#
#
#@pytest.fixture()
#def mock_get_db() -> Session:
#    """Fixture for mocking dependencies.get_db"""
#    session = Mock(spec=Session)
#    return session
#
#
#def test_get_by_id_author_not_found(mock_get_db):
#    """Test that get_by_id returns 404 http exception when author with a particular id does not exist"""
#
#    with pytest.raises(HTTPException) as e:
#        with patch.object(
#            author_plain, "get_by_author_id", return_value=None
#        ) as mock_method:
#            get_by_id(author_id=1, db=mock_get_db)
#            mock_method.assert_called_once_with(db=mock_get_db, id=1)
#        assert e.value.status_code == 404
#
#
#def test_get_by_id_author_exists(mock_get_db):
#    """Test that get_by_id successfully returns author details when author with a particular id exists"""
#    mock_author_id = 1
#    mock_author = Author(id=mock_author_id, name="test", email="test@test.com")
#
#    with patch.object(
#        author_plain, "get_by_author_id", return_value=mock_author
#    ) as mock_method:
#        author = get_by_id(author_id=mock_author_id, db=mock_get_db)
#        mock_method.assert_called_once_with(db=mock_get_db, id=mock_author_id)
#        assert author.id == mock_author_id
#        assert author.name == "test"
#        assert author.email == "test@test.com"
#