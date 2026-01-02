##
## EPITECH PROJECT, 2025
## AREA
## File description:
## authSpotify
##

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import httpx
from urllib.parse import urlencode
from app import oauthDbConfig, models, database, security, schemas


router = APIRouter(prefix="/auth", tags=["auth"])

SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_ME_URL = "https://api.spotify.com/v1/me"

@router.get("/spotify/login")
def logWithSpotify(db: Session = Depends(database.get_db)):
    config = oauthDbConfig.OauthDbConfig.get_service(db, "spotify")
    if not config:
        raise HTTPException(500, "Spotify oauth not configured")

    params = {
        "client_id": config.client_id,
        "redirect_uri": config.redirect_uri,
        "response_type": "code",
        "scope": "user-read-email",
    }

    spotify_url = f"{SPOTIFY_AUTH_URL}?{urlencode(params)}"
    return RedirectResponse(spotify_url)



@router.get("/spotify/callback")
async def spotify_callback(code: str, user_id: int, db: Session = Depends(database.get_db)):
    config = oauthDbConfig.OauthDbConfig.get_service(db, "spotify")
    if not config:
        raise HTTPException(500, "Spotify oauth not configured")

    async with httpx.AsyncClient() as client:
        res = await client.post(
            SPOTIFY_TOKEN_URL,
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

    service = db.query(models.Service).filter(models.Service.name == "spotify").first()

    oauthDbConfig.OauthDbConfig.save_user(
        db = db,
        user_id = user_id,
        service_id = service.id,
        access_token = tokens["access_token"],
        refresh_token = tokens.get("refresh_token")
    )

    headers = {"Authorization": f"Bearer {tokens['access_token']}"}

    async with httpx.AsyncClient() as client:
        user_info = await client.get(SPOTIFY_ME_URL, headers=headers)

    if user_info.status_code != 200:
        raise HTTPException(400, "Spotify Error")

    return {
        "message": "Spotify login success!",
        "spotify_user": user_info.json()
    }
