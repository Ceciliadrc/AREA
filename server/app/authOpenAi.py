##
## EPITECH PROJECT, 2025
## AREA
## File description:
## authOpenAi
##

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import httpx
from urllib.parse import urlencode
from app import oauthDbConfig, models, database, security, schemas


router = APIRouter(prefix="/auth", tags=["auth"])

OPENAI_AUTH_URL = "https://auth.openai.com/oauth/authorize"
OPENAI_TOKEN_URL = "https://auth.openai.com/oauth/token"

@router.get("/openai/login")
def logWithOpenai(db: Session = Depends(database.get_db)):
    config = oauthDbConfig.OauthDbConfig.get_service(db, "openai")
    if not config:
        raise HTTPException(500, "OpenAi oauth not configured")

    params = {
        "client_id": config.client_id,
        "redirect_uri": config.redirect_uri,
        "response_type": "code",
        "scope": "openid",
    }

    openai_url = f"{OPENAI_AUTH_URL}?{urlencode(params)}"
    return RedirectResponse(openai_url)



@router.get("/openai/callback")
async def openai_callback(code: str, user_id: int, db: Session = Depends(database.get_db)):
    config = oauthDbConfig.OauthDbConfig.get_service(db, "openai")
    if not config:
        raise HTTPException(500, "OpenAi oauth not configured")

    async with httpx.AsyncClient() as client:
        res = await client.post(
            OPENAI_TOKEN_URL,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "client_id": config.client_id,
                "client_secret": config.client_secret,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": config.redirect_uri
            }
        )

    if res.status_code != 200:
        raise HTTPException(400, "OpenAi Error")

    tokens = res.json()

    service = db.query(models.Service).filter(models.Service.name == "openai").first()

    oauthDbConfig.OauthDbConfig.save_user(
        db = db,
        user_id = user_id,
        service_id = service.id,
        access_token = tokens["access_token"],
        refresh_token = tokens.get("refresh_token")
    )

    return {
        "message": "OpenAi login success!",
        "tokens":tokens
    }
