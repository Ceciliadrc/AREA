from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, database, security
from app.schemas import UserRegister, UserLogin
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
def register(user_data: UserRegister, db: Session = Depends(database.get_db)):

    existing_email = db.query(models.User).filter(models.User.email == user_data.email).first()
    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Email already use"
        )

    existing_user = db.query(models.User).filter(models.User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already use"
        )

    hashed = security.hash_password(user_data.password)

    user = models.User(
        username=user_data.username,
        email=user_data.email,
        password=hashed
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    token_expire = timedelta(minutes= 60 * 24)
    access_token = security.create_access(
        data={"sub": user.email},
        expires_delta=token_expire
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "username": user.username
    }

@router.post("/login")
def login(user_data: UserLogin, db: Session = Depends(database.get_db)):

    user = security.authenticate_user(db, user_data.email, user_data.password)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token_expire = timedelta(minutes= 60 * 24)
    access_token = security.create_access(
        data={"sub": user.email},
        expires_delta=token_expire
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "username": user.username
    }

@router.post("/verify")
def verify_token(token: str):
    decode = security.decode_access(token)
    if decode is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )
    return {"valid": True, "email": decode.get("sub")}