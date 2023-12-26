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
from fastapi import FastAPI, APIRouter
from app.settings import DB_URI  # Assuming DB_URI is your MongoDB connection string

# Assuming 'app' was previously defined as FastAPI instance (since it's used in decorators)
app = FastAPI()

# replace 'DATABASE_URL' from the SQLAlchemy setup with 'DB_URI' for pymongo
client = MongoClient(DB_URI)
db = client["database_name"]  # You should replace 'database_name' with your actual database name

# create book_collection or any other collection you need
book_collection = db["book_collection"]  # Replace 'book_collection' with your actual collection name

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


def recreate_database():
    # Assuming DATABASE_URL will be a MongoDB connection string
    client = MongoClient(DATABASE_URL)
    
    # Here, 'mydatabase' is the database name. Replace it with your actual database name.
    db_name = 'mydatabase'
    
    # Drop the database
    client.drop_database(db_name)
    
    # Create new collections if necessary. Collection creation in MongoDB is implicit,
    # so you only need to specify the collection names if you need to do some setup,
    # such as creating indexes. For this example, let's assume we have a collection 'books'.
    db = client[db_name]
    books_collection = db['books']
    
    # If you have to set up indexes or other properties on your new collections, do it here.
    # For example:
    # books_collection.create_index([("title", pymongo.ASCENDING)])


recreate_database()

root_router = APIRouter()
app = FastAPI()


@app.get("/")
def root():
    return {"message": "Sample books API is online"}


app.include_router((api_v1.api_router))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
