from app.db.database import SessionLocal
from fastapi import Request
from pymongo import MongoClient


def get_db():
    client = MongoClient()  # Replace with your connection string if needed
    db = client['your_database_name']  # Replace with your database name
    try:
        yield db
    finally:
        client.close()

