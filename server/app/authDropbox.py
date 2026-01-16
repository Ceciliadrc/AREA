##
## EPITECH PROJECT, 2026
## AREA
## File description:
## authDropbox
##

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import httpx
from urllib.parse import urlencode
import os
from app import models, database

router = APIRouter(prefix="/auth", tags=["auth"])

DROPBOX_AUTH_URL = "https://www.dropbox.com/oauth2/authorize"
DROPBOX_TOKEN_URL = "https://api.dropboxapi.com/oauth2/token"

class DropboxOAuthConfig:
    client_id = os.getenv("DROPBOX_CLIENT_ID")
    client_secret = os.getenv("DROPBOX_CLIENT_SECRET")
    redirect_uri = os.getenv("DROPBOX_REDIRECT_URI")

@router.get("/dropbox/login")
def logWithDropbox(user_id: int):
    if not DropboxOAuthConfig.client_id or not DropboxOAuthConfig.client_secret:
        raise HTTPException(500, "Dropbox OAuth not configured in .env")

    params = {
        "client_id": DropboxOAuthConfig.client_id,
        "redirect_uri": DropboxOAuthConfig.redirect_uri,
        "response_type": "code",
        "token_access_type": "offline",
        "state": str(user_id)
    }

    dropbox_url = f"{DROPBOX_AUTH_URL}?{urlencode(params)}"
    return RedirectResponse(dropbox_url)

@router.get("/dropbox/callback")
async def dropbox_callback(state: str, code: str, db: Session = Depends(database.get_db)):
    if not DropboxOAuthConfig.client_id or not DropboxOAuthConfig.client_secret:
        raise HTTPException(500, "Dropbox OAuth not configured in .env")
    
    user_id = int(state)

    async with httpx.AsyncClient() as client:
        res = await client.post(
            DROPBOX_TOKEN_URL,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "client_id": DropboxOAuthConfig.client_id,
                "client_secret": DropboxOAuthConfig.client_secret,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": DropboxOAuthConfig.redirect_uri
            }
        )

    if res.status_code != 200:
        raise HTTPException(400, f"Dropbox Error: {res.text}")

    tokens = res.json()

    service = db.query(models.Service).filter(models.Service.name == "dropbox").first()

    from app.oauthDbConfig import OauthDbConfig
    OauthDbConfig.save_user(
        db=db,
        user_id=user_id,
        service_id=service.id,
        access_token=tokens["access_token"],
        refresh_token=tokens.get("refresh_token")
    )

    return {
        "message": "Dropbox login successful!",
        "tokens":tokens
    }
