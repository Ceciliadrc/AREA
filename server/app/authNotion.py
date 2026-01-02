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
from app import oauthDbConfig, models, database, security, schemas


router = APIRouter(prefix="/auth", tags=["auth"])

NOTION_AUTH_URL = "https://api.notion.com/v1/oauth/authorize"
NOTION_TOKEN_URL = "https://api.notion.com/v1/oauth/token"

@router.get("/notion/login")
def logWithNotion(db: Session = Depends(database.get_db)):
    config = oauthDbConfig.OauthDbConfig.get_service(db, "notion")
    if not config:
        raise HTTPException(500, "Notion oauth not configured")

    params = {
        "client_id": config.client_id,
        "redirect_uri": config.redirect_uri,
        "response_type": "code",
        "owner": "user",
    }

    notion_url = f"{NOTION_AUTH_URL}?{urlencode(params)}"
    return RedirectResponse(notion_url)


@router.get("/notion/callback")
async def notion_callback(code: str, user_id: int, db: Session = Depends(database.get_db)):
    config = oauthDbConfig.OauthDbConfig.get_service(db, "notion")
    if not config:
        raise HTTPException(500, "Notion oauth not configured")

    async with httpx.AsyncClient() as client:
        res = await client.post(
            NOTION_TOKEN_URL,
            auth=(config.client_id, config.client_secret),
            data={
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": config.redirect_uri
            }
        )

    if res.status_code != 200:
        raise HTTPException(400, "Notion Error")

    tokens = res.json()

    service = db.query(models.Service).filter(models.Service.name == "notion").first()

    oauthDbConfig.OauthDbConfig.save_user(
        db = db,
        user_id = user_id,
        service_id = service.id,
        access_token = tokens["access_token"]
    )

    return {
        "message": "Notion login success!",
        "notion_user": res.json()
    }
