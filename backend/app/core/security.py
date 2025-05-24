from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from app.config import settings

def create_jwt_token(data: dict) -> str:
    expiration = datetime.utcnow() + timedelta(seconds = settings.JWT_EXPIRATION_TIME)
    data.update({"exp": expiration})
    
    return jwt.encode(data, settings.JWT_SECRET_KEY, algorithm="HS256")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)