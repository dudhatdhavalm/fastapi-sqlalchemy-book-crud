from typing import List, Optional
from pydantic import BaseModel 
from datetime import date

class BookBase(BaseModel):
    title: Optional[str] = None
    pages: Optional[int] = None
    created_at : date = date.today()

class BookCreate(BookBase):
    title: str
    pages: int
    author_id : int
    
    class Config:
        orm_mode = True