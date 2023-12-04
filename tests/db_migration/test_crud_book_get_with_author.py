#
#import pytest
#from app.models.book import Book
#from app.models.author import Author
#from app.crud.crud_book import *
#from typing import Any, Dict, List, TypeVar, Union
#from datetime import date
#from sqlalchemy.orm import Session
#
#
#class CRUDBook:
#    def get_with_author(self, db: Session) -> List[Book]:
#        books = (
#            db.query(
#                Book.id,
#                Book.title,
#                Book.pages,
#                Book.created_at,
#                Book.author_id,
#                Author.name.label("author_name"),
#            )
#            .join(Book, Author.id == Book.author_id)
#            .all()
#        )
#
#        return books
#