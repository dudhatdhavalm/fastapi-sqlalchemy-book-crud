from datetime import date
from typing import Optional

from fastapi import APIRouter, FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.api import api_v1
from app.models.book import Base, Book
from app.settings import DATABASE_URL
import uvicorn
from pymongo import MongoClient
from pymongo.errors import CollectionInvalid
from fastapi import FastAPI

app = FastAPI()  # Assuming this is defined somewhere in your larger code base

# Assuming DATABASE_URL is in MongoDB URI format like: 'mongodb://localhost:27017/mydatabase'
DATABASE_URL = "mongodb://localhost:27017/mydatabase"  # Replace with your MongoDB URL

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


def recreate_database():
    client = MongoClient(DATABASE_URL)
    db = client['mydatabase']  # Replace 'mydatabase' with your database name

    # In MongoDB, collections are created lazily, so they are only truly created when the first document is inserted.
    # However, you could ensure that all indexes you might need are created here,
    # which would implicitly create the collection if it didn't exist already.
    # Example: db['books'].create_index([('title', pymongo.ASCENDING)], unique=True)

    # Ensure the collections exist by creating them without any documents
    # This is not typically necessary, but is here to replicate the SQLAlchemy behavior.
    try:
        db.create_collection('books')
        # You could create other collections if needed
        # db.create_collection('authors')
    except CollectionInvalid:
        # Collection already exists
        pass

    client.close()


recreate_database()

root_router = APIRouter()


# Function to establish a MongoDB connection and list collections

@app.get("/")
def root():
    client = MongoClient(DATABASE_URL)
    db = client.get_default_database()  # Get the default database
    collections = db.list_collection_names()  # This lists all collection names
    client.close()  # Close the MongoClient connection
    return {"message": "Sample books API is online", "collections": collections}
app = FastAPI()


app.include_router((api_v1.api_router))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
