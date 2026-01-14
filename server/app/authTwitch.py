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
from dotenv import load_dotenv
from app import oauthDbConfig, models, database, security, schemas

load_dotenv()

router = APIRouter(prefix="/auth", tags=["auth"])

TWITCH_AUTH_URL = "https://id.twitch.tv/oauth2/authorize"
TWITCH_TOKEN_URL = "https://id.twitch.tv/oauth2/token"
TWITCH_USER_URL = "https://api.twitch.tv/helix/users"

@router.get("/twitch/login")
def logWithTwitch(user_id: int, db: Session = Depends(database.get_db)):
    config = oauthDbConfig.OauthDbConfig.get_service(db, "twitch")
    if not config:
        raise HTTPException(500, "Twitch oauth not configured")

    params = {
        "client_id": config.client_id,
        "redirect_uri": config.redirect_uri,
        "response_type": "code",
        "scope": "user:read:email",
        "state": str(user_id)
    }

    twitch_url = f"{TWITCH_AUTH_URL}?{urlencode(params)}"
    return RedirectResponse(twitch_url)



@router.get("/twitch/callback")
async def twitch_callback(state: str, code: str, user_id: int, db: Session = Depends(database.get_db)):
    config = oauthDbConfig.OauthDbConfig.get_service(db, "twitch")
    if not config:
        raise HTTPException(500, "Twitch oauth not configured")
    
    user_id = int(state)
    
    async with httpx.AsyncClient() as client:
        res = await client.post(
            TWITCH_TOKEN_URL,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "client_id": config.client_id,
                "client_secret": config.client_secret,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": config.redirect_uri
            }
        )

    tokens = res.json()

    service = db.query(models.Service).filter(models.Service.name == "twitch").first()

    oauthDbConfig.OauthDbConfig.save_user(
        db = db,
        user_id = user_id,
        service_id = service.id,
        access_token = tokens["access_token"],
        refresh_token = tokens.get("refresh_token")
    )

    headers = {"Authorization": f"Bearer {tokens['access_token']}",
                "Client-Id": config.client_id,
    }

    async with httpx.AsyncClient() as client:
        user_info = await client.get(TWITCH_USER_URL, headers=headers)

    if user_info.status_code != 200:
        raise HTTPException(400, "Twitch Error")

    return {
        "message": "Twitch login success!",
        "twitch_user": user_info.json()
    }
