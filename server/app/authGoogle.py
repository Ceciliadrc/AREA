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
import httpx
import os
from app import database, models

router = APIRouter(prefix="/auth", tags=["auth"])

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://accounts.google.com/o/oauth2/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"

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
