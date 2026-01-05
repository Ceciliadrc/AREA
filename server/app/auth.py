from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import models, database, security
from app.schemas import UserRegister, UserLogin

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
def register(user_data: UserRegister, db: Session = Depends(database.get_db)):
    if db.query(models.User).filter(models.User.email == user_data.email).first():
        return {"error": "Email already in use"}
    
    hashed = security.hash_password(user_data.password)
    
    user = models.User(
        username=user_data.username,
        email=user_data.email,
        password=hashed
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return {
        "success": True,
        "message": "Registration successful",
        "user_id": user.id,
        "username": user.username
    }

@router.post("/login")
def login(user_data: UserLogin, db: Session = Depends(database.get_db)):

    user = security.authenticate_user(db, user_data.email, user_data.password)
    
    if not user:
        return {"error": "Email or password incorrect"}
    
    return {
        "success": True,
        "message": "Login successful",
        "user_id": user.id,
        "username": user.username
    }
