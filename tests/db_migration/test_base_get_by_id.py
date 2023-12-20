#from sqlalchemy.orm import Session
#
#import pytest
#from app.crud.base import *
#from typing import Any
#from unittest.mock import Mock
#from app.crud.base import CRUDBase
#
#
#@pytest.fixture()
#def mock_session() -> Mock:
#    return Mock(spec=Session)
#
#
#@pytest.fixture()
#def mock_model() -> Mock:
#    mock = Mock()
#    mock.id = 1  # Set attribute for model instance
#    return mock
#
#
#def test_get_by_id_no_errors(mock_session: Mock, mock_model: Any) -> None:
#    crud = CRUDBase(model=mock_model)
#    result = crud.get_by_id(mock_session, id=1)
#    assert result is not None
#
#
#def test_get_by_id_non_existant_id(mock_session: Mock, mock_model: Any) -> None:
#    crud = CRUDBase(model=mock_model)
#    result = crud.get_by_id(
#        mock_session, id=99999
#    )  # Id which does not exist in the database
#    assert result is None
#
#
#def test_get_by_id_incorrect_id_type(mock_session: Mock, mock_model: Any) -> None:
#    crud = CRUDBase(model=mock_model)
#    with pytest.raises(
#        Exception
#    ):  # Sqlalchemy will raise an exception with wrong id type
#        result = crud.get_by_id(mock_session, id="invalid_id")
#