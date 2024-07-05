from sqlalchemy import Column, Integer, ForeignKey
from database.database import Base

class BooksCategories(Base):
    __tablename__ = "books_categories"
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey('books.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))