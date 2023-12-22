from app.db.database import SessionLocal
from fastapi import Request
from pymongo import MongoClient

client = MongoClient('localhost', 27017)  # Adjust the connection parameters as needed


def get_db():
    db = client['your_database_name']  # Replace with your actual database name
    try:
        yield db
    finally:
        client.close()

