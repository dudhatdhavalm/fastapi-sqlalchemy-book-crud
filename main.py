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

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


def recreate_database():
    Base.metadata.create_all(engine)


recreate_database()

root_router = APIRouter()
app = FastAPI()


@root_router.get("/")
def root():
    return {"message": "Sample books API is online"}

app.include_router((api_v1.api_router))
