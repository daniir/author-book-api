from fastapi import HTTPException, status
from sqlalchemy.orm import sessionmaker
from models.author import Author
from schemas.userSchema import UserCreate, UserLogin
from schemas.responseMessage import ResponseMessage, ResponseAuthMessage
from utils.hashing import hashPassword, checkPasswordHashed
from utils.token import generateToken

class AuthService():

    def __init__(self, db: sessionmaker) -> None:
        self.db = db


    def __getUserByEmail(self, email: str) -> Author | None:
        userExist = self.db.query(Author).filter(Author.email == email).first()
        return userExist

    def createNewUser(self, user: UserCreate) -> ResponseMessage:
        user_db = self.__getUserByEmail(user.email)
        if user_db is not None:
            return ResponseMessage(
                status=status.HTTP_400_BAD_REQUEST,
                message="user already exists"
            )
        
        passwdHash = hashPassword(user.password)
        user.password = passwdHash

        new_user = Author(
            # first_name = user.first_name,
            # last_name = user.last_name,
            # email = user.email,
            # password = passwdHash
            **user.model_dump()
        )

        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)

        return ResponseMessage(
                status=status.HTTP_201_CREATED,
                message="new user added"
            )


    def loginUser(self, user: UserLogin) -> ResponseAuthMessage | None:
        user_db = self.__getUserByEmail(user.email)
        if user_db is None:
            return None
        
        passwdMatch = checkPasswordHashed(user.password, user_db.password)
        if not passwdMatch:
            return ResponseAuthMessage(
                status=status.HTTP_403_FORBIDDEN,
                message="invalid email/password, please try again",
                token=None
            )
        
        jwt = generateToken({"sub": str(user_db.id),"userEmail": user_db.email})
        
        return ResponseAuthMessage(
                status=status.HTTP_200_OK,
                message="ok",
                token=f"bearer {jwt}"
            )
