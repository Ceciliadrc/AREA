##
## EPITECH PROJECT, 2026
## AREA
## File description:
## authTrello
##

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from urllib.parse import urlencode
import httpx
import os
from app import database, models

router = APIRouter(prefix="/auth", tags=["auth"])

TRELLO_AUTH_URL = "https://trello.com/1/authorize"
TRELLO_USERINFO_URL = "https://api.trello.com/1/members/me"

class TrelloOAuthConfig:
    api_key = os.getenv("TRELLO_API_KEY", "87c2d227a4c327ae4de99603af6b71ed")
    redirect_uri = os.getenv("TRELLO_REDIRECT_URI", "http://localhost:8080/auth/trello/callback")

@router.get("/trello/login")
def logWithTrello(user_id: int):
    if not TrelloOAuthConfig.api_key:
        raise HTTPException(500, "TRELLO_API_KEY not configured in .env")

    params = {
        "key": TrelloOAuthConfig.api_key,
        "response_type": "token",  # vu que cest implicit Flow = token direct
        "scope": "read,write",
        "expiration": "never",
        "name": "AREA App",
        "callback_method": "fragment",
        "return_url": TrelloOAuthConfig.redirect_uri,
        "state": str(user_id)
    }

    trello_url = f"{TRELLO_AUTH_URL}?{urlencode(params)}"
    return RedirectResponse(trello_url)

@router.get("/trello/callback")
async def trello_callback(state: str, token: str = None, db: Session = Depends(database.get_db)):
    if not TrelloOAuthConfig.api_key or not TrelloOAuthConfig.api_secret:
        raise HTTPException(500, "Trello OAuth not configured in .env")
    
    user_id = int(state)

    if not token:
        raise HTTPException(400, "No token received from Trello")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.trello.com/1/members/me",
                params={
                    "key": TrelloOAuthConfig.api_key,
                    "token": token
                },
                timeout=10.0
            )
            if response.status_code != 200:
                raise HTTPException(400, "Invalid Trello token")
                
            user_info = response.json()
            
    except Exception as e:
        raise HTTPException(400, f"Error token Trello")
    
    service = db.query(models.Service).filter(models.Service.name == "trello").first()
    
    if service:
        from app.oauthDbConfig import OauthDbConfig
        OauthDbConfig.save_user(
            db=db,
            user_id=user_id,
            service_id=service.id,
            access_token=token,
            refresh_token=None,
        )
    return {
        "message": "Trello login success!",
        "user_info": {
            "id": user_info.get("id"),
            "username": user_info.get("username"),
        },
    }
