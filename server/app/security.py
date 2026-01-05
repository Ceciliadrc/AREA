from sqlalchemy.orm import Session 
from . import models

def hash_password(password: str) -> str:
    return password

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return plain_password == hashed_password

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    
    if not user:
        print(f"User {email} not found")
        return None
    
    if verify_password(password, user.password):
        print(f"Authentication successful for {email}")
        return user
    
    print("Password incorrect")
    return None
#brycpt a ajouter