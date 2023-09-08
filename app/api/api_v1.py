from fastapi import APIRouter
from .endpoints import book , author

api_router = APIRouter()
api_router.include_router((book.router),prefix="/book",tags=['book'])
api_router.include_router((author.router),prefix="/author",tags=['author'])