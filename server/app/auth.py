from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from urllib.parse import urlencode
from app import models, database, security, schemas


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=schemas.UserResponse)
def register(username: str, email: str, password: str, db: Session = Depends(database.get_db)):

    if db.query(models.User).filter(models.User.email == email).first():
        return {"error": "Email already use"}
    
    hashed = security.hash_password(password)
    
    new_user = models.User(
        username=username,
        email=email,
        password=hashed
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "Registration successful",
        "user_id": new_user.id,
        "username": new_user.username
    }

@router.post("/login", response_model=schemas.UserResponse)
def login(email: str, password: str, db: Session = Depends(database.get_db)):

    user = security.authenticate_user(db, email, password)
    
    if not user:
        return {"error": "Email or password incorect"}
    
    return {
        "message": "Login successful",
        "user_id": user.id,
        "username": user.username
    }
