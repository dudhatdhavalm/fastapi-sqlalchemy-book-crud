#from unittest.mock import MagicMock, patch
#
#from app.api.endpoints.author import *
#
#
#from unittest.mock import MagicMock, patch
#
#import pytest
#
#
## Test to ensure recreate_database function doesn't throw any errors
#def test_recreate_database():
#    with patch("app.models.author.Base.metadata.create_all") as mock_create_all:
#        recreate_database()
#        # Check if create_all has been called
#        mock_create_all.assert_called_once()
#