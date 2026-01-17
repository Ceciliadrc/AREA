##
## EPITECH PROJECT, 2026
## AREA
## File description:
## authMicrosoft
##

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from urllib.parse import urlencode
import httpx
import os
from app import database, models

router = APIRouter(prefix="/auth", tags=["auth"])

MICROSOFT_AUTH_URL = "https://login.microsoftonline.com/common/oauth2/v2.0/authorize"
MICROSOFT_TOKEN_URL = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
MICROSOFT_USERINFO_URL = "https://graph.microsoft.com/v1.0/me"

class MicrosoftOAuthConfig:
    client_id = os.getenv("MICROSOFT_CLIENT_ID")
    client_secret = os.getenv("MICROSOFT_CLIENT_SECRET")
    redirect_uri = os.getenv("MICROSOFT_REDIRECT_URI")

@router.get("/microsoft/login")
def logWithMicrosoft(user_id: int):
    if not MicrosoftOAuthConfig.client_id or not MicrosoftOAuthConfig.client_secret:
        raise HTTPException(500, "Microsoft OAuth not configured in .env")

    params = {
        "client_id": MicrosoftOAuthConfig.client_id,
        "redirect_uri": MicrosoftOAuthConfig.redirect_uri,
        "response_type": "code",
        "scope": "User.Read offline_access",
        "response_mode": "query",
        "state": str(user_id)
    }

    microsoft_url = f"{MICROSOFT_AUTH_URL}?{urlencode(params)}"
    return RedirectResponse(microsoft_url)

@router.get("/microsoft/callback")
async def microsoft_callback(state: str, code: str, db: Session = Depends(database.get_db)):
    if not MicrosoftOAuthConfig.client_id or not MicrosoftOAuthConfig.client_secret:
        raise HTTPException(500, "Microsoft OAuth not configured in .env")

    user_id = int(state)

    async with httpx.AsyncClient() as client:
        res = await client.post(
            MICROSOFT_TOKEN_URL,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=urlencode({
                "client_id": MicrosoftOAuthConfig.client_id,
                "client_secret": MicrosoftOAuthConfig.client_secret,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": MicrosoftOAuthConfig.redirect_uri
            })
        )

    if res.status_code != 200:
        raise HTTPException(400, "Failed to get token from Microsoft")

    tokens = res.json()
    access_token=tokens.get("access_token")
    refresh_token=tokens.get("refresh_token")

    if not access_token:
        raise HTTPException(400, f"No access token for Microsoft")

    async with httpx.AsyncClient() as client:
        user_info_res = await client.get(
            MICROSOFT_USERINFO_URL,
            headers=({
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            })
        )
    if user_info_res.status_code != 200:
        raise HTTPException(400, f"No user info from Microsoft")

    user_info = user_info_res.json()
    service = db.query(models.Service).filter(models.Service.name == "microsoft").first()

    from app.oauthDbConfig import OauthDbConfig
    OauthDbConfig.save_user(
        db=db,
        user_id=user_id,
        service_id=service.id,
        access_token=access_token,
        refresh_token=refresh_token
    )

    return {
        "message": "Microsoft login success!",
        "user_info": {
            "id": user_info.get("id"),
            "username": user_info.get("username"),
        },
        "access_token": access_token
    }
