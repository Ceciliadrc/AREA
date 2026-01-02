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
from app import oauthDbConfig, database, models
router = APIRouter(prefix="/auth", tags=["auth"])

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://accounts.google.com/o/oauth2/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"

@router.get("/google/login")
def logWithGoogle(db: Session = Depends(database.get_db)):
    config = oauthDbConfig.OauthDbConfig.get_service(db, "google")
    if not config:
        raise HTTPException(500, "Google oauth not configured")

    params = {
        "client_id": config.client_id,
        "redirect_uri": config.redirect_uri,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "consent"
    }

    google_url = f"{GOOGLE_AUTH_URL}?{urlencode(params)}"
    return RedirectResponse(google_url)


@router.get("/google/callback")
async def google_callback(code: str, user_id: int, db: Session = Depends(database.get_db)):

    config = oauthDbConfig.OauthDbConfig.get_service(db, "google")
    if not config:
        raise HTTPException(500, "Google oauth not configured")

    async with httpx.AsyncClient() as client:
        res = await client.post(
            GOOGLE_TOKEN_URL,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=urlencode({
                "client_id": config.client_id,
                "client_secret": config.client_secret,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": config.redirect_uri
            })
        )

    if res.status_code != 200:
        raise HTTPException(400, "Failed to get token from Google")

    tokens = res.json()

    service = db.query(models.Service).filter(models.Service.name == "google").first()

    oauthDbConfig.OauthDbConfig.save_user(
        db = db,
        user_id = user_id,
        service_id = service.id,
        access_token = tokens["access_token"],
        refresh_token = tokens.get("refresh_token")
    )

    headers = {"Authorization": f"Bearer {tokens['access_token']}"}

    async with httpx.AsyncClient() as client:
        user_info = await client.get(GOOGLE_USERINFO_URL, headers=headers)

    if user_info.status_code != 200:
        raise HTTPException(400, "Google Error")

    google_user = user_info.json()

    return {
        "message": "Google login success!",
        "google_user": google_user,
        "tokens": tokens
    }
