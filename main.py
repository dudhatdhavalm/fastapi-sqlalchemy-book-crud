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

DATABASE_NAME = 'your_database_name'  # Replace with your database name.
BOOK_COLLECTION_NAME = 'books'  # Replace with your collection name.

# Ensuring correct imports
client = MongoClient(DATABASE_URL)  # DATABASE_URL should be the MongoDB connection string.
db = client[DATABASE_NAME]

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)



def recreate_database():
    # Explicitly creating the 'books' collection if it doesn't exist and ensuring the index.
    db.create_collection(BOOK_COLLECTION_NAME)
    BookCollection(db, BOOK_COLLECTION_NAME)


recreate_database()

root_router = APIRouter()
app = FastAPI()


@app.get("/")
def root():
    return {"message": "Sample books API is online"}


app.include_router((api_v1.api_router))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
