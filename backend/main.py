##
## EPITECH PROJECT, 2025
## AREA
## File description:
## Oauth2Con
##

from fastapi import FastAPI, Request, HTTPException
from starlette.config import Config
import httpx
from urllib.parse import urlencode
from fastapi.responses import RedirectResponse
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()


GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://accounts.google.com/o/oauth2/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"


@app.get("/auth/google/login")
def logWithGoogle():
    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "consent"
    }

    google_url = f"{GOOGLE_AUTH_URL}?{urlencode(params)}"
    return RedirectResponse(google_url)


@app.get("/auth/google/callback")
async def google_callback(code: str):
    data = {
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "code": code,
        "grant_type": "authorization_code"
    }

    async with httpx.AsyncClient() as client:
        res = await client.post(
            GOOGLE_TOKEN_URL,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=urlencode({
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": GOOGLE_REDIRECT_URI
            })
        )

    if res.status_code != 200:
        raise HTTPException(400, "Failed to get token from Google")

    tokens = res.json()
    access_token = tokens["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}

    async with httpx.AsyncClient() as client:
        user_info = await client.get(GOOGLE_USERINFO_URL, headers=headers)

    if user_info.status_code != 200:
        raise HTTPException(400, "Error")

    google_user = user_info.json()

    return {
        "message": "Google login success!",
        "google_user": google_user,
        "tokens": tokens
    }