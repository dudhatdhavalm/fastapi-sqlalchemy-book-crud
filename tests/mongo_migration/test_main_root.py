from fastapi.testclient import TestClient

from main import *


import pytest
import pytest
from main import app

from main import app
from pymongo import MongoClient

client = MongoClient()
db = client.test_database
collection = db.test_collection

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() is not None
