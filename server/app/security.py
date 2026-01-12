import bcrypt
from sqlalchemy.orm import Session
from . import models
from sqlalchemy.orm import Session
from . import models, database
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/login")

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(models.User).filter(models.User.email == email).first()

    if not user:
        return None
    
    if verify_password(password, user.password):
        return user
    return None

def create_access(data: dict, expires_delta: Optional[timedelta] = None):
    encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes= 60 * 24)
    encode.update({"exp": expire})
    encode_jwt = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt

def decode_access(token: str):
    try:
        decode = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decode
    except JWTError:
        return None

def get_user(token: str = Depends(oauth2), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credentials not validate",
        headers={"WWW-Authenticate": "Bearer"}
    )

    decode = decode_access(token)
    if decode is None:
        raise credentials_exception

    email: str = decode.get("sub")
    if email is None:
        raise credentials_exception

    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise credentials_exception

    return user

def active_user(current_user: models.User = Depends(get_user)):
    return current_user