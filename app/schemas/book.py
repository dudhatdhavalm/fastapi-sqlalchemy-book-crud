from typing import List, Optional
from pydantic import BaseModel 
from datetime import date

class BookBase(BaseModel):
    title: Optional[str] = None
    pages: Optional[int] = None
    created_at : date = date.today()

class BookCreate(BaseModel):
    title: str
    pages: int
    author_id : int
    
    class Config:
        orm_mode = True
    
class BookInDBBase(BookBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class Books(BookInDBBase):
    pass

class BookUpdate(BaseModel):
    title: Optional[str] = None
    pages: Optional[int] = None
    author_id: Optional[int] = None