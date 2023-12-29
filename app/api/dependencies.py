from app.db.database import SessionLocal
from fastapi import Request
from pymongo import MongoClient


def get_db():
    client = MongoClient('localhost', 27017)  # or adjust the IP/port as needed
    try:
        db = client['your_database_name']  # replace 'your_database_name' with your actual database name
        yield db
    finally:
        client.close()

