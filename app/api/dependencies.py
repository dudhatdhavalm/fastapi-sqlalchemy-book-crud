
from app.db.database import SessionLocal
from fastapi import Request

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

