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
import os
from app import models, database

router = APIRouter(prefix="/auth", tags=["auth"])

GITHUB_AUTH_URL = "https://github.com/login/oauth/authorize"
GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"

class GithubOAuthConfig:
    client_id = os.getenv("GITHUB_CLIENT_ID")
    client_secret = os.getenv("GITHUB_CLIENT_SECRET")
    redirect_uri = os.getenv("GITHUB_REDIRECT_URI")

@router.get("/github/login")
def logWithGithub(user_id: int):
    if not GithubOAuthConfig.client_id or not GithubOAuthConfig.client_secret:
        raise HTTPException(500, "GitHub OAuth not configured in .env")

    params = {
        "client_id": GithubOAuthConfig.client_id,
        "redirect_uri": GithubOAuthConfig.redirect_uri,
        "scope": "user repo",
        "state": str(user_id)
    }

    github_url = f"{GITHUB_AUTH_URL}?{urlencode(params)}"
    return RedirectResponse(github_url)

@router.get("/github/callback")
async def github_callback(state: str, code: str, db: Session = Depends(database.get_db)):
    if not GithubOAuthConfig.client_id or not GithubOAuthConfig.client_secret:
        raise HTTPException(500, "GitHub OAuth not configured in .env")
    
    user_id = int(state)

    async with httpx.AsyncClient() as client:
        res = await client.post(
            GITHUB_TOKEN_URL,
            headers={"Accept": "application/json", "Content-Type": "application/x-www-form-urlencoded"},
            data={
                "client_id": GithubOAuthConfig.client_id,
                "client_secret": GithubOAuthConfig.client_secret,
                "code": code,
                "redirect_uri": GithubOAuthConfig.redirect_uri
            }
        )

    if res.status_code != 200:
        raise HTTPException(400, f"GitHub Error: {res.text}")

    tokens = res.json()

    if "access_token" not in tokens:
        raise HTTPException(400, "No access_token for GitHub")

    service = db.query(models.Service).filter(models.Service.name == "github").first()

    from app.oauthDbConfig import OauthDbConfig
    OauthDbConfig.save_user(
        db=db,
        user_id=user_id,
        service_id=service.id,
        access_token=tokens["access_token"],
        refresh_token=tokens.get("refresh_token")
    )

    return {
        "message": "GitHub login successful!",
        "tokens":tokens
    }