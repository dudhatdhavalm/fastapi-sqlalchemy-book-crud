#
#
#import pytest
#
#from main import *
#from fastapi.testclient import TestClient
#import pytest
#
## Note: The FastAPI app instance should be in the same file where this test is placed
## If not, you'll need to import it from the right module.
#
#
#@pytest.fixture(scope="module")
#def test_client():
#    client = TestClient(app)
#    yield client
#    client.close()
#
#
#def test_root(test_client):
#    """
#    Test if the root function returns the expected response.
#    """
#    response = test_client.get("/")
#    assert response.status_code == 200
#    assert response.json() is not None
#