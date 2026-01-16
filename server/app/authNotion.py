##
## EPITECH PROJECT, 2025
## AREA
## File description:
## authNotion
##

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import httpx
from urllib.parse import urlencode
import os
from app import models, database

router = APIRouter(prefix="/auth", tags=["auth"])

NOTION_AUTH_URL = "https://api.notion.com/v1/oauth/authorize"
NOTION_TOKEN_URL = "https://api.notion.com/v1/oauth/token"

class NotionOAuthConfig:
    client_id = os.getenv("NOTION_CLIENT_ID")
    client_secret = os.getenv("NOTION_CLIENT_SECRET")
    redirect_uri = os.getenv("NOTION_REDIRECT_URI")

@router.get("/notion/login")
def logWithNotion(user_id: int):
    if not NotionOAuthConfig.client_id or not NotionOAuthConfig.client_secret:
        raise HTTPException(500, "Notion OAuth not configured in .env")

    params = {
        "client_id": NotionOAuthConfig.client_id,
        "redirect_uri": NotionOAuthConfig.redirect_uri,
        "response_type": "code",
        "owner": "user",
        "state": f"user-{user_id}"  # FORCE string avec préfixe
    }

    notion_url = f"{NOTION_AUTH_URL}?{urlencode(params)}"
    return RedirectResponse(notion_url)

@router.get("/notion/callback")
async def notion_callback(state: str, code: str, db: Session = Depends(database.get_db)):
    if not NotionOAuthConfig.client_id or not NotionOAuthConfig.client_secret:
        raise HTTPException(500, "Notion OAuth not configured in .env")
    
    # Extrait user_id de "user-1"
    try:
        user_id = int(state.split("-")[1])
    except:
        raise HTTPException(400, f"Invalid state: {state}")

    async with httpx.AsyncClient() as client:
        res = await client.post(
            NOTION_TOKEN_URL,
            auth=(NotionOAuthConfig.client_id, NotionOAuthConfig.client_secret),
            data={
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": NotionOAuthConfig.redirect_uri
            }
        )

    if res.status_code != 200:
        raise HTTPException(400, f"Notion Error: {res.text}")

    tokens = res.json()

    service = db.query(models.Service).filter(models.Service.name == "notion").first()

    from app.oauthDbConfig import OauthDbConfig
    OauthDbConfig.save_user(
        db=db,
        user_id=user_id,
        service_id=service.id,
        access_token=tokens["access_token"]
    )

    return {
        "message": "Notion login success!",
        "user_id": user_id,
        "service": "notion",
        "access_token_preview": tokens.get("access_token", "")[:20] + "..." if tokens.get("access_token") else None
    }