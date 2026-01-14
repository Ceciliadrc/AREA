##
## EPITECH PROJECT, 2026
## AREA
## File description:
## authGithub
##

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import httpx
from urllib.parse import urlencode
from app import oauthDbConfig, models, database, security, schemas

router = APIRouter(prefix="/auth", tags=["auth"])

GITHUB_AUTH_URL = "https://github.com/login/oauth/authorize"
GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"

@router.get("/github/login")
def logWithGithub(db: Session = Depends(database.get_db)):
    config = oauthDbConfig.OauthDbConfig.get_service(db, "github")
    if not config:
        raise HTTPException(500, "Github oauth not configured")

    params = {
        "client_id": config.client_id,
        "redirect_uri": config.redirect_uri,
        "scope" : "user",
    }

    github_url = f"{GITHUB_AUTH_URL}?{urlencode(params)}"
    return RedirectResponse(github_url)



@router.get("/github/callback")
async def github_callback(code: str, user_id: int, db: Session = Depends(database.get_db)):
    config = oauthDbConfig.OauthDbConfig.get_service(db, "github")
    if not config:
        raise HTTPException(500, "Github oauth not configured")

    async with httpx.AsyncClient() as client:
        res = await client.post(
            GITHUB_TOKEN_URL,
            headers={"Accept": "application/json", "Content-Type": "application/x-www-form-urlencoded"},
            data={
                "client_id": config.client_id,
                "client_secret": config.client_secret,
                "code": code,
                "redirect_uri": config.redirect_uri
            }
        )

    if res.status_code != 200:
        raise HTTPException(400, "Github Error")

    tokens = res.json()

    if "access_token" not in tokens:
        raise HTTPException(400, "No access_token for Github")

    service = db.query(models.Service).filter(models.Service.name == "github").first()

    if not service:
        raise HTTPException(500, "Github service not found")

    oauthDbConfig.OauthDbConfig.save_user(
        db = db,
        user_id = user_id,
        service_id = service.id,
        access_token = tokens["access_token"],
        refresh_token = tokens.get("refresh_token")
    )

    return {
        "message": "Github login success!",
        "tokens":tokens
    }
