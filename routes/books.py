from fastapi import APIRouter, Path, Body, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from typing import List
from sqlalchemy.orm import Session
from database.database import get_db
from schemas.bookSchema import BookInfo, BookWithAuthor, BookUpdateCategories
from services.bookService import BookService
from schemas.bookSchema import BookCreate, BookUpdate
from schemas.responseMessage import PayloadJwtResponse
from utils.token import validateToken

route = APIRouter(
    prefix="/books",
    tags= ["Books"],
    dependencies=[Depends(get_db)]
)

@route.get("/", response_model=List[BookInfo])
def getBooks(db: Session = Depends(get_db)):

    books = BookService(db).getAllBooks()
    if books is None:
        return HTTPException(status.HTTP_200_OK, detail="[]")
    
    return books
    
@route.get("/{id}", response_model=BookWithAuthor)
def getBook(
        id: int = Path(..., gt=0),
        db: Session = Depends(get_db)
    ):

    book = BookService(db).getBookById(id)
    if book is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Book not found")
    
    return book

    
@route.post("/")
def addBook(
    book: BookCreate = Body(...),
    db: Session = Depends(get_db),
    payload: PayloadJwtResponse = Depends(validateToken)
    ):

    if payload is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                            detail="Unauthorized, you need to login")
    if payload is False:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE,
                            detail="invalid token type")

    resp = BookService(db).addNewBook(book, int(payload.sub))

    return JSONResponse(
        status_code=resp.status,
        content=resp.message
    )
    
@route.put("/{id}")
def updateBook(
    id: int = Path(..., gt=0),
    book: BookUpdate = Body(...),
    db: Session = Depends(get_db),
    payload: PayloadJwtResponse = Depends(validateToken)):

    if payload is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                            detail="Unauthorized, you need to login")
    
    if payload is False:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE,
                            detail="invalid token type")
    
    resp = BookService(db).updateExistentBook(id, book, int(payload.sub))

    if resp is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="only the owner its authorized to update the book"
        )
    
    return JSONResponse(
            status_code=resp.status,
            content=resp.message
        )
        

@route.patch("/categories/{id}")
def updateBookCategories(
    id: int = Path(..., gt=0),
    bookCategorie: BookUpdateCategories = Body(...),
    db: Session = Depends(get_db),
    payload: PayloadJwtResponse = Depends(validateToken)):

    if payload is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                            detail="Unauthorized, you need to login")
    
    if payload is False:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE,
                            detail="invalid token type")

    resp = BookService(db).updateBookCategories(id, bookCategorie, int(payload.sub))
    
    if resp is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    
    return JSONResponse(
            status_code=resp.status,
            content=resp.message
        )

@route.delete("/{id}")
def deleteBook(
    id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    payload: PayloadJwtResponse = Depends(validateToken)):

    if payload is None:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                                detail="Unauthorized, you need to login")
    
    if payload is False:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE,
                            detail="invalid token type")
    
    resp = BookService(db).deleteBook(id, int(payload.sub))
    
    return JSONResponse(
            status_code=resp.status,
            content=resp.message
        )