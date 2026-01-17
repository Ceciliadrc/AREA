##
## EPITECH PROJECT, 2025
## AREA
## File description:
## authGoogle
##

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from urllib.parse import urlencode
from datetime import timedelta
import httpx
import os
import uuid
from app import database, models, security

from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

router = APIRouter(prefix="/auth", tags=["auth"])

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://accounts.google.com/o/oauth2/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")

class GoogleOAuthConfig:
    client_id = os.getenv("GOOGLE_CLIENT_ID")
    client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
    redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")

@router.get("/google/login")
def logWithGoogle(user_id: int):
    if not GoogleOAuthConfig.client_id or not GoogleOAuthConfig.client_secret:
        raise HTTPException(500, "Google OAuth not configured in .env")

    params = {
        "client_id": GoogleOAuthConfig.client_id,
        "redirect_uri": GoogleOAuthConfig.redirect_uri,
        "response_type": "code",
        "scope": "openid email profile https://www.googleapis.com/auth/gmail.readonly",
        "access_type": "offline",
        "prompt": "consent",
        "state": str(user_id)
    }

    google_url = f"{GOOGLE_AUTH_URL}?{urlencode(params)}"
    return RedirectResponse(google_url)

@router.get("/google/callback")
async def google_callback(state: str, code: str, db: Session = Depends(database.get_db)):
    if not GoogleOAuthConfig.client_id or not GoogleOAuthConfig.client_secret:
        raise HTTPException(500, "Google OAuth not configured in .env")
    
    user_id = int(state)

    async with httpx.AsyncClient() as client:
        res = await client.post(
            GOOGLE_TOKEN_URL,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=urlencode({
                "client_id": GoogleOAuthConfig.client_id,
                "client_secret": GoogleOAuthConfig.client_secret,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": GoogleOAuthConfig.redirect_uri
            })
        )

    if res.status_code != 200:
        raise HTTPException(400, "Failed to get token from Google")

    tokens = res.json()

    service = db.query(models.Service).filter(models.Service.name == "google").first()

    from app.oauthDbConfig import OauthDbConfig
    OauthDbConfig.save_user(
        db=db,
        user_id=user_id,
        service_id=service.id,
        access_token=tokens["access_token"],
        refresh_token=tokens.get("refresh_token")
    )

    headers = {"Authorization": f"Bearer {tokens['access_token']}"}

    return {
        "message": "Google login success!",
        "tokens": tokens
    }

class GoogleTokenBody(dict):
    pass

@router.post("google/token")
def google_token_login(payload: dict, db: Session = Depends(database.get_db)):
    if not GOOGLE_CLIENT_ID:
        raise HTTPException(500, "GOOGLE_CLIENT_ID missing in env")
    
    raw_id_token = payload.get("id_token")
    if not raw_id_token:
        raise HTTPException(400, "Missing id_token")
    
    try:
        claims = id_token.verify_oauth2_token(
            raw_id_token,
            google_requests.Request(),
            GOOGLE_CLIENT_ID
        )
    except Exception:
        raise HTTPException(401, "Invalid Google ID token")
    
    email = claims.get("email")
    google_sub = claims.get("sub")
    if not email or not google_sub:
        raise HTTPException(400, "Google token missing email/sub")
    
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        base = (claims.get("name") or email.split("@")[0]).replace(" ", "").lower()
        username = base

        i = 1
        while db.query(models.User).filter(models.User.username == username).first():
            i += 1
            username = f"{base}{i}"

        random_pw = str(uuid.uuid4())
        user = models.User(
            username=username,
            email=email,
            password=security.hash_password(random_pw)
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    service = db.query(models.Service).filter(models.Service.name == "google").first()
    if service:
        existing_link = db.query(models.UserOauth).filter(
            models.UserOauth.user_id == user.id,
            models.UserOauth.service_id == service.id
        ).first()

        if existing_link:
            existing_link.provider_user_id = google_sub
        else:
            db.add(models.UserOauth(
                user_id=user.id,
                service_id=service.id,
                provide_user_id=google_sub
            ))
        db.commit()

    token_expire = timedelta(minutes=60 * 24)
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
