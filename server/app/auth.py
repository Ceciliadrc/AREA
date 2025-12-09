from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import httpx
from urllib.parse import urlencode
import os
from dotenv import load_dotenv
from app import models, database, security, schemas

load_dotenv()

router = APIRouter(prefix="/auth", tags=["auth"])

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://accounts.google.com/o/oauth2/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"

@router.post("/register", response_model=schemas.UserResponse)
def register(username: str, email: str, password: str, db: Session = Depends(database.get_db)):

    if db.query(models.User).filter(models.User.email == email).first():
        return {"error": "Email already use"}
    
    hashed = security.hash_password(password)
    
    new_user = models.User(
        username=username,
        email=email,
        hashed_password=hashed
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

@router.get("/google/login")
def logWithGoogle():
    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "consent"
    }

    google_url = f"{GOOGLE_AUTH_URL}?{urlencode(params)}"
    return RedirectResponse(google_url)


@router.get("/google/callback")
async def google_callback(code: str):
    data = {
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "code": code,
        "grant_type": "authorization_code"
    }

    async with httpx.AsyncClient() as client:
        res = await client.post(
            GOOGLE_TOKEN_URL,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=urlencode({
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": GOOGLE_REDIRECT_URI
            })
        )

    if res.status_code != 200:
        raise HTTPException(400, "Failed to get token from Google")

    tokens = res.json()
    access_token = tokens["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}

    async with httpx.AsyncClient() as client:
        user_info = await client.get(GOOGLE_USERINFO_URL, headers=headers)

    if user_info.status_code != 200:
        raise HTTPException(400, "Error")

    google_user = user_info.json()

    return {
        "message": "Google login success!",
        "google_user": google_user,
        "tokens": tokens
    }