from passlib.context import CryptContext

__pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hashPassword(password: str) -> str:
    passwdHash = __pwd_context.hash(password)
    return passwdHash

def checkPasswordHashed(password: str, passwordHash: str) -> bool:
    return __pwd_context.verify(password, passwordHash)