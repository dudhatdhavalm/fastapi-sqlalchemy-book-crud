#import pytest
#
#
#import pytest
#from fastapi.testclient import TestClient
#
#from main import *
#from main import app
#
#client = TestClient(app)
#
#
#def test_root_endpoint():
#    """
#    Test to ensure that the root endpoint returns a status code of 200
#    and the expected response structure, without making a connection
#    to the actual database.
#    """
#    response = client.get("/")
#    assert response.status_code == 200
#    assert response.json() == {"message": "Sample books API is online"}
#