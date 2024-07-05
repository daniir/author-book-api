from fastapi import status
from sqlalchemy.orm import sessionmaker, joinedload
from typing import List
from models.book import Book
from models.category import Category
from schemas.bookSchema import BookInfo, BookCreate, BookUpdate, BookUpdateCategories, BookWithAuthor
from schemas.responseMessage import ResponseMessage

class BookService():

    def __init__(self, db: sessionmaker) -> None:
        self.db = db


    def getAllBooks(self) -> List[BookInfo]:
        booksList = self.db.query(Book).all()
        return booksList

    def getBookById(self, id: int) -> BookWithAuthor | None:
        bookResponse = self.db.query(
            Book
            ).options(
                joinedload(Book.author),
                joinedload(Book.categories)
            ).filter(
                Book.id == id
            ).first()

        return bookResponse
    
    def getBookByIdAndAuthorId(self, id: int, authorId: int) -> BookInfo | None:
        bookResponse = self.db.query(
            Book
        ).filter(
            Book.id == id,
            Book.author_id == authorId
        ).first()
        return bookResponse

    def addNewBook(
            self,
            book: BookCreate,
            author_id: int
        ) -> ResponseMessage:
        new_book = Book(
                title = book.title,
                synopsis = book.synopsis,
                published_date = book.published_date,
                author_id = author_id,
            )
        
        self.db.add(new_book)
        self.db.commit()
        self.db.refresh(new_book)

        for id in book.categories:
            category = self.db.query(Category).filter(Category.id == id).first()
            if category:
                new_book.categories.append(category)
        self.db.commit()

        return ResponseMessage(
            status=status.HTTP_201_CREATED,
            message="new book added"
        )
    
    def updateExistentBook(
            self,
            id: int,
            book: BookUpdate,
            author_id: int) -> ResponseMessage:
        
        db_book = self.getBookByIdAndAuthorId(id, author_id)
        if db_book is None:
            return None
        
        db_book.title = book.title
        db_book.synopsis = book.synopsis
        db_book.published_date = book.published_date
        self.db.commit()

        return ResponseMessage(
            status=status.HTTP_200_OK,
            message="Book updated"
        )
        
    def updateBookCategories(
            self,
            id: int,
            bookCategorie: BookUpdateCategories,
            author_id: int) -> ResponseMessage:
        db_book = self.getBookByIdAndAuthorId(id, author_id)
        if db_book is None:
            return None
        
        if bookCategorie.isRemove is False:
            setNewCategories = { id for id in bookCategorie.categories }
            setActualCategories = { category.id for category in db_book.categories }
            newCategories = setNewCategories - setActualCategories

            for id in newCategories:
                db_category = self.db.query(Category).filter(
                    Category.id == id
                ).first()
                if db_category:
                    db_book.categories.append(db_category)
            self.db.commit()
        
        else:
            setNewCategories = { id for id in bookCategorie.categories }
            setActualCategories = { category.id for category in db_book.categories }
            newCategories = setActualCategories - setNewCategories
            
            for id in newCategories:
                db_category = self.db.query(Category).filter(
                    Category.id == id
                ).first()
                if db_category:
                    db_book.categories.remove(db_category)
            self.db.commit()

        return ResponseMessage(
            status=status.HTTP_200_OK,
            message="Categories updated"
        )

    def deleteBook(
            self,
            id: int,
            author_id: int) -> ResponseMessage | None:
        
        db_book = self.getBookByIdAndAuthorId(id, author_id)

        if db_book is None:
            return None
        
        self.db.delete(db_book)
        self.db.commit()

        return ResponseMessage(
            status=status.HTTP_200_OK,
            message="Book deleted"
        )
