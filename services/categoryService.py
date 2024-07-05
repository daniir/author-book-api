from fastapi import status
from typing import List
from sqlalchemy.orm import sessionmaker
from models.category import Category
from schemas.categorySchema import CategoryInfo
from schemas.responseMessage import ResponseMessage

class CategoryService():
    def __init__(self, db: sessionmaker) -> None:
        self.db = db
    
    def getAllCategories(self) -> List[CategoryInfo] | None:
        categoryList = self.db.query(Category).all()
        return categoryList

    def getCategoryById(self, id: int) -> CategoryInfo:
        categoryResponse = self.db.query(Category).filter(Category.id == id).first()
        return categoryResponse

    def addNewCategory(self, name: str) -> ResponseMessage:
        new_category = Category(
            name = name
        )

        self.db.add(new_category)
        self.db.commit()
        self.db.refresh(new_category)

        return ResponseMessage(
            status=status.HTTP_201_CREATED,
            message="Category added"
        )

    def updateExistentCategory(self, 
                               id: int, 
                               name: str) -> ResponseMessage | None:
        db_category = self.getCategoryById(id)
        if db_category is None:
            return None
        
        db_category.name = name
        self.db.commit()

        return ResponseMessage(
            status=status.HTTP_200_OK,
            message="Category updated"
        )
    
    def deleteExistentCategory(self, 
                               id: int) -> ResponseMessage | None:
        db_category = self.getCategoryById(id)
        if db_category is None:
            return None
        
        self.db.delete(db_category)
        self.db.commit()

        return ResponseMessage(
            status=status.HTTP_200_OK,
            message="Category deleted"
        )