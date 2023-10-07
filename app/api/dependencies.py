from app.db.database import SessionLocal
from fastapi import Request
from pymongo import MongoClient



def get_db():
    client = MongoClient('localhost', 27017)
    db = client.test_database
    try:
        yield db
    finally:
        client.close()

