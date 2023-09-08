from typing import List, Optional
from pydantic import BaseModel 
from datetime import date

class AuthorBase(BaseModel):
    name: Optional[str] = None

class AuthorCreate(AuthorBase):
    ...
        
    class Config:
        orm_mode = True