from fastapi import APIRouter, Path, Body, Depends,status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List
from sqlalchemy.orm import Session
from database.database import get_db
from schemas.categorySchema import CategoryBase, CategoryInfo
from services.categoryService import CategoryService

route = APIRouter(
    prefix="/category",
    tags=["Category"],
    dependencies=[Depends(get_db)]
)

@route.get("/", response_model=List[CategoryInfo])
def getCategories(
    db: Session = Depends(get_db)):
    categories = CategoryService(db).getAllCategories()
    if categories is None:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder("[]")
        )
    
    return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder(categories)
        )

@route.post("/")
def createCategory(
    category: CategoryBase = Body(...),
    db: Session = Depends(get_db)):

    resp = CategoryService(db).addNewCategory(category.name)

    return JSONResponse(
        status_code=resp.status,
        content=resp.message
    )

@route.put("/{id}")
def updateCategory(
    id: int = Path(...,gt=0),
    category: CategoryBase = Body(...),
    db: Session = Depends(get_db)):

    resp = CategoryService(db).updateExistentCategory(id, category.name)

    if resp is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with id {id} not found"
        )
    
    return JSONResponse(
        status_code=resp.status,
        content=resp.message
    )
    
@route.delete("/{id}")
def deleteCategory(id: int = Path(..., gt=0),
                   db: Session = Depends(get_db)):
    
    resp = CategoryService(db).deleteExistentCategory(id)

    if resp is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with id {id} not found"
        )
    
    return JSONResponse(
        status_code=resp.status,
        content=resp.message
    )