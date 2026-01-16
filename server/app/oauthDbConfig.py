##
## EPITECH PROJECT, 2025
## AREA
## File description:
## oauthDbConfig
##

from sqlalchemy.orm import Session
from app import models
from datetime import datetime, timedelta
import json

class OauthDbConfig:
    def get_service(db: Session, service_name: str):
        service = db.query(models.Service).filter(models.Service.name == service_name).first()

        if not service or not service.oauth_config:
            return None

        return service.oauth_config

    def save_user(
        db: Session,
        user_id: int,
        service_id: int,
        access_token: str,
        refresh_token: str = None,
        provider_user_id: str = None
    ):
        token_exist = db.query(models.UserOauth).filter(
            models.UserOauth.user_id == user_id,
            models.UserOauth.service_id == service_id
        ).first()

        if token_exist:
            token_exist.access_token = access_token
            token_exist.refresh_token = refresh_token or token_exist.refresh_token
            if provider_user_id:
                token_exist.provider_user_id = provider_user_id
        else:
            new_token = models.UserOauth(
                    user_id = user_id,
                    service_id = service_id,
                    access_token = access_token,
                    refresh_token = refresh_token,
                    provider_user_id = provider_user_id
            )
            db.add(new_token)
        db.commit()

    def get_user(db: Session, user_id: int, service_name: str):
        service = db.query(models.Service).filter(models.Service.name == service_name).first()

        if not service:
            return None

        token = db.query(models.UserOauth).filter(
            models.UserOauth.user_id == user_id,
            models.UserOauth.service_id == service.id
        ).first()

        return token

    def default_service(db: Session):
        default_init = [
            {"name": "google", "display_name": "Google"},
            {"name": "twitch", "display_name": "Twitch"},
            {"name": "notion", "display_name": "Notion"},
            {"name": "openai", "display_name": "Openai"},
            {"name": "github", "display_name": "Github"},
            {"name": "dropbox", "display_name": "Drop box"},
        ]

        for data in default_init:
            if not db.query(models.Service).filter(models.Service.name == data["name"]).first():
                service = models.Service(
                    name = data["name"],
                    display_name = data["display_name"]
                )
                db.add(service)
        db.commit()