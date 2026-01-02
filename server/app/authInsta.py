##
## EPITECH PROJECT, 2025
## AREA
## File description:
## authInsta
##

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import httpx
from urllib.parse import urlencode
from app import oauthDbConfig, models, database, security, schemas


router = APIRouter(prefix="/auth", tags=["auth"])

INSTAGRAM_AUTH_URL = "https://api.instagram.com/oauth/authorize"
INSTAGRAM_TOKEN_URL = "https://api.instagram.com/oauth/access_token"

@router.get("/instagram/login")
def logWithInstagram(db: Session = Depends(database.get_db)):
    config = oauthDbConfig.OauthDbConfig.get_service(db, "instagram")
    if not config:
        raise HTTPException(500, "Instagram oauth not configured")

    params = {
        "client_id": config.client_id,
        "redirect_uri": config.redirect_uri,
        "response_type": "code",
        "scope": "user_profile",
    }

    instagram_url = f"{INSTAGRAM_AUTH_URL}?{urlencode(params)}"
    return RedirectResponse(instagram_url)



@router.get("/instagram/callback")
async def instagram_callback(code: str, user_id: int, db: Session = Depends(database.get_db)):
    config = oauthDbConfig.OauthDbConfig.get_service(db, "instagram")
    if not config:
        raise HTTPException(500, "Instagram oauth not configured")

    async with httpx.AsyncClient() as client:
        res = await client.post(
            INSTAGRAM_TOKEN_URL,
            data={
                "client_id": config.client_id,
                "client_secret": config.client_secret,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": config.redirect_uri
            }
        )
    if res.status_code != 200:
        raise HTTPException(400, "Instagram Error")

    tokens = res.json()

    service = db.query(models.Service).filter(models.Service.name == "instagram").first()

    oauthDbConfig.OauthDbConfig.save_user(
        db = db,
        user_id = user_id,
        service_id = service.id,
        access_token = tokens["access_token"]
    )

    return {
        "message": "Instagram login success!",
        "instagram_user": res.json()
    }
