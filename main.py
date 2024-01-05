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
from fastapi import FastAPI

# MongoDB connection URL
MONGODB_URL = "mongodb://localhost:27017"

client = MongoClient(MONGODB_URL)
# Replace 'your_db_name' with the actual name of your MongoDB database
db = client.your_db_name
# Replace 'books' with the actual name of your collection within the 'your_db_name' database
books_collection = db.books

# Assuming DATABASE_URL is in the form 'mongodb://localhost:27017/mydatabase'

# In pymongo, you don't need to declare a 'Base' or a set of 'tables' as in SQLAlchemy.
# MongoDB creates new collections automatically as you insert documents into them.

# Declare the collections you plan to use (in place of SQLAlchemy tables)
# For example purposes, we will assume there's a 'books' collection.
collections_to_create = ['books']

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


def recreate_database():
    client = MongoClient(DATABASE_URL)
    db_name = DATABASE_URL.split('/')[-1]  # Extract database name
    db = client[db_name]
    
    for collection_name in collections_to_create:
        if collection_name not in db.list_collection_names():
            # In MongoDB, you don't actually need to 'create' a collection
            # as it is created automatically when data is inserted.
            # However, you can use below line if you need to create an empty collection.
            db.create_collection(collection_name)
            
    client.close()


recreate_database()

root_router = APIRouter()


@app.get("/")
def root():
    return {"message": "Sample books API is online"}
app = FastAPI()


app.include_router((api_v1.api_router))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
