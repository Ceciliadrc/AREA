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
from app import oauthDbConfig, models, database, security, schemas

router = APIRouter(prefix="/auth", tags=["auth"])

DROPBOX_AUTH_URL = "https://www.dropbox.com/oauth2/authorize"
DROPBOX_TOKEN_URL = "https://api.dropboxapi.com/oauth2/token"
DROPBOX_USER_URL = "https://api.dropboxapi.com/2/users/get_current_account"

@router.get("/dropbox/login")
def logWithDropbox(user_id: int, db: Session = Depends(database.get_db)):
    config = oauthDbConfig.OauthDbConfig.get_service(db, "dropbox")
    if not config:
        raise HTTPException(500, "Dropbox oauth not configured")

    params = {
        "client_id": config.client_id,
        "redirect_uri": config.redirect_uri,
        "response_type": "code",
        "token_access_type": "offline",
        "state": str(user_id)
    }

    dropbox_url = f"{DROPBOX_AUTH_URL}?{urlencode(params)}"
    return RedirectResponse(dropbox_url)



@router.get("/dropbox/callback")
async def dropbox_callback(state: str, code: str, user_id: int, db: Session = Depends(database.get_db)):
    config = oauthDbConfig.OauthDbConfig.get_service(db, "dropbox")
    if not config:
        raise HTTPException(500, "Dropbox oauth not configured")

    user_id = int(state)

    async with httpx.AsyncClient() as client:
        res = await client.post(
            DROPBOX_TOKEN_URL,
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
        user_info = await client.get(DROPBOX_USER_URL, headers=headers)

    if user_info.status_code != 200:
        raise HTTPException(400, "Dropbox Error")

    return {
        "message": "Dropbox login success!",
        "dropbox_user": user_info.json()
    }
