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
from pymongo.collection import Collection
from fastapi import FastAPI

# Connect to MongoDB
client = MongoClient(DATABASE_URL)
db = client.get_default_database()

# Assuming 'books' is the collection we want to create.
# In MongoDB, collections are created lazily, so you do not need to explicitly
# create them. However, creating an index or inserting a document will.
collection: Collection = db['books']

client = MongoClient(DATABASE_URL)
db = client.get_database()  # You can specify a database name if it's not in the DATABASE_URL

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


def recreate_database():
    # You should define the collections based on your application's needs
    # In this example, 'books' is a collection inferred from the context provided
    book_collection: Collection = db.get_collection('books')

    # If you have specific indexes or unique constraints to apply, you can do it here
    # For example, creating a unique index on 'isbn' field of 'books' collection if 'isbn' is a field in Book schema
    # book_collection.create_index([('isbn', pymongo.ASCENDING)], unique=True)
    
    # The following just ensures that the 'books' collection exists
    # As MongoDB creates collections automatically upon first document insertion, the following line is optional
    book_collection = db.create_collection('books')

    # If the book schema defines more collections or indexes, set them up here
    # Repeat the book_collection.create_index(...) call with appropriate fields for other indexes

    # If there are any other tasks you perform during database recreation, such as seeding data, include them here


@app.get("/")
def root():
    return {"message": "Sample books API is online"}


recreate_database()

root_router = APIRouter()
app = FastAPI()


app.include_router((api_v1.api_router))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
