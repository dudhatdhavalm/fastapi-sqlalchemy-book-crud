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


def recreate_database():
    # Start client
    client = MongoClient(DATABASE_URL)
    
    # Get the database
    db = client.get_database()

    # As the actual collection creation happens 
    # when the first document is inserted, 
    # just print a message here confirming the database is accessible 
    print(f"Database {db.name} is ready.")


recreate_database()

root_router = APIRouter()
app = FastAPI()


@app.get("/")
def root():
    return {"message": "Sample books API is online"}


app.include_router((api_v1.api_router))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
