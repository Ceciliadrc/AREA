##
## EPITECH PROJECT, 2025
## AREA
## File description:
## authTwitch
##

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import httpx
from urllib.parse import urlencode
import os
from app import models, database

router = APIRouter(prefix="/auth", tags=["auth"])

TWITCH_AUTH_URL = "https://id.twitch.tv/oauth2/authorize"
TWITCH_TOKEN_URL = "https://id.twitch.tv/oauth2/token"
TWITCH_USER_URL = "https://api.twitch.tv/helix/users"

class TwitchOAuthConfig:
    client_id = os.getenv("TWITCH_CLIENT_ID")
    client_secret = os.getenv("TWITCH_CLIENT_SECRET")
    redirect_uri = os.getenv("TWITCH_REDIRECT_URI")

@router.get("/twitch/login")
def logWithTwitch(user_id: int):
    if not TwitchOAuthConfig.client_id or not TwitchOAuthConfig.client_secret:
        raise HTTPException(500, "Twitch OAuth not configured in .env")

    params = {
        "client_id": TwitchOAuthConfig.client_id,
        "redirect_uri": TwitchOAuthConfig.redirect_uri,
        "response_type": "code",
        "scope": "user:read:email",
        "state": str(user_id)
    }

    twitch_url = f"{TWITCH_AUTH_URL}?{urlencode(params)}"
    return RedirectResponse(twitch_url)

@router.get("/twitch/callback")
async def twitch_callback(state: str, code: str, db: Session = Depends(database.get_db)):
    if not TwitchOAuthConfig.client_id or not TwitchOAuthConfig.client_secret:
        raise HTTPException(500, "Twitch OAuth not configured in .env")
    
    user_id = int(state)

    async with httpx.AsyncClient() as client:
        res = await client.post(
            TWITCH_TOKEN_URL,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "client_id": TwitchOAuthConfig.client_id,
                "client_secret": TwitchOAuthConfig.client_secret,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": TwitchOAuthConfig.redirect_uri
            }
        )

    tokens = res.json()

    service = db.query(models.Service).filter(models.Service.name == "twitch").first()

    from app.oauthDbConfig import OauthDbConfig
    OauthDbConfig.save_user(
        db=db,
        user_id=user_id,
        service_id=service.id,
        access_token=tokens["access_token"],
        refresh_token=tokens.get("refresh_token")
    )

    headers = {
        "Authorization": f"Bearer {tokens['access_token']}",
        "Client-Id": TwitchOAuthConfig.client_id
    }
    return {
        "message": "Twitch login success!",
        "tokens":tokens
    }