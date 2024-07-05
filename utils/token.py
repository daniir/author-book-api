from fastapi import Cookie
from typing import Annotated
from datetime import datetime, timedelta
from jose import jwt
from settings.settings import JWT_SECRET
from schemas.responseMessage import PayloadJwtResponse

def generateToken(data: list) -> str:
    token = jwt.encode(data, JWT_SECRET, algorithm="HS256")
    return token

def validateToken(
        access_token: Annotated[str | None, Cookie()] = None
    ) -> PayloadJwtResponse | None | bool:
    if access_token is None:
        return None
    
    token = access_token.split()
    if(token[0] != "bearer"):
        return False

    payload = jwt.decode(token[1], JWT_SECRET, algorithms=["HS256"])
    return PayloadJwtResponse(
        sub=payload["sub"],
        userEmail=payload["userEmail"]
    )