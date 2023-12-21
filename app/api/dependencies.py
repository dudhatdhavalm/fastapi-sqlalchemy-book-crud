from app.db.database import SessionLocal
from fastapi import Request
from pymongo import MongoClient


def get_db():
    client = MongoClient('mongodb://localhost:27017')  # This URI should be configured according to your MongoDB setup
    db = client["mydatabase"]  # Replace "mydatabase" with the name of your database
    try:
        yield db
    finally:
        client.close()

