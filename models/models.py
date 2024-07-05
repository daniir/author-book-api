from models import author, book, category, books_categories
from database.database import engine

def createTables():
    author.Base.metadata.create_all(bind=engine)
    book.Base.metadata.create_all(bind=engine)
    category.Base.metadata.create_all(bind=engine)
    books_categories.Base.metadata.create_all(bind=engine)