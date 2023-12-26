from app.db.database import SessionLocal
from fastapi import Request
from pymongo import MongoClient

# Assuming 'MONGO_URI' is an environment variable containing your MongoDB connection string.
# You should define 'MONGO_URI' in your environment or replace it accordingly.
MONGO_URI = "your_mongo_connection_string"


# PyMongo doesn't have a session concept like SQLAlchemy which automatically closes,
# so we'll manage the client instance directly using 'try...finally'.

def get_db():
    client = MongoClient(MONGO_URI)
    try:
        db = client.your_db_name  # replace 'your_db_name' with the name of your database
        yield db
    finally:
        client.close()

