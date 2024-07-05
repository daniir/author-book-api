from fastapi import APIRouter, Body, Depends, Response, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database.database import get_db
from services.authService import AuthService
from schemas.userSchema import UserCreate, UserLogin

route = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    dependencies=[Depends(get_db)]
)

@route.post("/signup", status_code=status.HTTP_201_CREATED)
def createUser(
        user: UserCreate = Body(...),
        db: Session = Depends(get_db)
    ):
    resp = AuthService(db).createNewUser(user)
    return JSONResponse(
        status_code=resp.status,
        content=resp.message
    )

@route.post("/login",
            status_code=status.HTTP_200_OK)
def createUserSession(user: UserLogin,
                      response: Response,
                      db: Session = Depends(get_db)):
    
    resp = AuthService(db).loginUser(user)

    if resp is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found, please try to sign up"
        )

    if resp.token is None:
        return JSONResponse(
            status_code=resp.status,
            content=resp.message
        )
    
    response = JSONResponse(
        status_code=resp.status,
        content=resp.message)
    
    response.set_cookie(key="access_token", value=resp.token)

    return response

@route.post("/logout", status_code=status.HTTP_200_OK)
def logoutUserSession(response: Response):
    response = JSONResponse(
        status_code=status.HTTP_200_OK,
        content="logout successfully")

    response.delete_cookie(key="access_token")

    return response