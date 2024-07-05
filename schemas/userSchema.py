from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    first_name: str = Field(max_length=(50))
    last_name: str = Field(max_length=(50))

class UserData(BaseModel):
    email: EmailStr

class UserCreate(UserBase, UserData):
    password: str = Field(min_length=8)

class UserLogin(UserData):
    password: str