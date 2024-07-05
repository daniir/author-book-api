from pydantic import BaseModel
from typing import List
from datetime import date
from .userSchema import UserBase
from .categorySchema import CategoryBase

class BookBase(BaseModel):
    title: str
    synopsis: str
    published_date: date

class BookCategories(BaseModel):
    categories: List[int]

class BookInfo(BookBase):
    id: int

    class ConfigDict:
        orm_mode = True

class BookWithAuthor(BookInfo):
    author: UserBase
    categories: List[CategoryBase]

    class ConfigDict:
        orm_mode = True

class BookCreate(BookBase, BookCategories):
    pass

class BookUpdate(BookBase):
    pass

class BookUpdateCategories(BookCategories):
    isRemove: bool