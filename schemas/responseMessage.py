from pydantic import BaseModel, EmailStr

class ResponseMessage(BaseModel):
    status: int
    message: str

class ResponseAuthMessage(ResponseMessage):
    token: str | None

class PayloadJwtResponse(BaseModel):
    sub: str
    userEmail: EmailStr