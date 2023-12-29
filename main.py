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

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


# Assuming DATABASE_URL is in the form of 'mongodb://localhost:27017/mydatabase' 

def recreate_database():
    # Parse the connection URL (Assuming it's a MongoDB URI)
    client = MongoClient(DATABASE_URL)
    
    # Get the database from the URI
    db_name = DATABASE_URL.split('/')[-1]
    db = client[db_name]
    
    # Example of ensuring a collection exists by simply accessing it.
    # Collections and databases in MongoDB are created lazily - they exist when they are first accessed.
    books_collection = db['books']
    
    # You could also create indexes like this if needed
    # books_collection.create_index([('title', pymongo.ASCENDING)], unique=True)


recreate_database()

root_router = APIRouter()
app = FastAPI()


@app.get("/")
def root():
    return {"message": "Sample books API is online"}


app.include_router((api_v1.api_router))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
