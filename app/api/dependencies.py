from app.db.database import SessionLocal
from fastapi import Request
from pymongo import MongoClient


def get_db():
    client = MongoClient()  # add your connection string if needed
    db = client['your_database_name']  # replace 'your_database_name' with your actual database name
    try:
        yield db
    finally:
        client.close()

