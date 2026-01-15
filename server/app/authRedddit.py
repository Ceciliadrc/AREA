##
## EPITECH PROJECT, 2026
## AREA
## File description:
## authRedddit
##


from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import httpx
from urllib.parse import urlencode
from app import oauthDbConfig, models, database, security, schemas

router = APIRouter(prefix="/auth", tags=["auth"])

REDDIT_AUTH_URL = "https://www.reddit.com/api/v1/authorize"
REDDIT_TOKEN_URL = "https://www.reddit.com/api/v1/access_token"
REDDIT_USERINFO_URL = "https://oauth.reddit.com/api/v1/me"

@router.get("/reddit/login")
def logWithReddit(user_id: int,db: Session = Depends(database.get_db)):
    config = oauthDbConfig.OauthDbConfig.get_service(db, "reddit")
    if not config:
        raise HTTPException(500, "Reddit oauth not configured")

    params = {
        "client_id": config.client_id,
        "redirect_uri": config.redirect_uri,
        "response_type": "code",
        "scope": "identity",
        "state": str(user_id),
        "duration": "permanent"
    }

    reddit_url = f"{REDDIT_AUTH_URL}?{urlencode(params)}"
    return RedirectResponse(reddit_url)



@router.get("/reddit/callback")
async def reddit_callback(code: str, state: str, db: Session = Depends(database.get_db)):
    config = oauthDbConfig.OauthDbConfig.get_service(db, "reddit")
    if not config:
        raise HTTPException(500, "Reddit oauth not configured")

    user_id = int(state)
    auth = httpx.BasicAuth(config.client_id, config.client_secret)

    async with httpx.AsyncClient() as client:
        res = await client.post(
            REDDIT_TOKEN_URL,
            auth=auth,
            headers={"User-Agent": "YourApp/1.0 by YourUsername", "Content-Type": "application/x-www-form-urlencoded"},
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": config.redirect_uri
            }
        )

    if res.status_code != 200:
        raise HTTPException(400, "Reddit Error")

    tokens = res.json()

    if "access_token" not in tokens:
        raise HTTPException(400, "No access_token for Reddit")

    headers={"Authorization": f"Bearer {tokens['access_token']}", "User-Agent": "YourApp/1.0 by YourUsername"}
    async with httpx.AsyncClient() as client:
        user_res = await client.get(REDDIT_USERINFO_URL, headers=headers)

    reddit_user = user_res.json()

    service = db.query(models.Service).filter(models.Service.name == "reddit").first()

    if not service:
        raise HTTPException(500, "Reddit service not found")

    oauthDbConfig.OauthDbConfig.save_user(
        db = db,
        user_id = user_id,
        service_id = service.id,
        access_token = tokens["access_token"],
        refresh_token = tokens.get("refresh_token")
    )

    return {
        "message": "Reddit login success!",
        "reddit_user": reddit_user,
        "tokens":tokens
    }
