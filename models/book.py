from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base
from datetime import date

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))
    synopsis = Column(Text)
    published_date = Column(Date)
    created_at = Column(Date, default=date.today())
    author_id = Column(Integer,
                       ForeignKey("authors.id"))
    author = relationship("Author", back_populates="books")
    categories = relationship("Category",
                              secondary="books_categories",
                              back_populates="books")