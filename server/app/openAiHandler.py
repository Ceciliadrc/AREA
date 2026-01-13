##
## EPITECH PROJECT, 2026
## AREA
## File description:
## OpenAiHandler
##

import httpx
from sqlalchemy.orm import Session
from datetime import datetime
from app import models, oauthDbConfig
from typing import Dict
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class OpenAiHandler:
    def __init__(self):
        self.service_name = "openai"

    def get_auth(self, user_id: int, db: Session):
        user_token = oauthDbConfig.OauthDbConfig.get_user(db, user_id, self.service_name)

        if user_token and user_token.access_token:
            return {"access_token": user_token.access_token, "user_id": user_id}
        return None

    def check_action(self, action: models.Action, user_id: int, db: Session) -> bool:

        if action.name == "ask_question":
            auth = self.get_auth(user_id, db)
            if not auth:
                return False
            return self.ask_question(auth, user_id, db, action)

        return False

    def ask_question(self, auth: Dict, user_id: int, db: Session, action: models.Action) -> bool:
        areas = db.query(models.Area).filter_by(user_id=user_id, action_id=action.id).all()
        if not areas:
            return False
        action_detected = False
        for area in areas:
            params = area.parameters or {}
            question = params.get("question")
            answered = params.get("answered", False)
            if question and not answered:
                params["asked_at"] = datetime.now().isoformat()
                area.parameters = params
                action_detected = True
        if action_detected:
            db.commit()
            return True
        return False

    def execute_reaction(self, reaction: models.Reaction, user_id: int, db: Session) -> bool:
        area = db.query(models.Area).filter_by(user_id=user_id, reaction_id=reaction.id).first()

        if not area:
            return False

        params = area.parameters or {}
        question = params.get("question")
        if not question:
            return False
        answer = self.ask_openai(question)
        if not answer:
            return False

        params["answer"] = answer
        params["answered"] = True
        params["answered_at"] = datetime.now().isoformat()
        area.parameters = params
        db.commit()
        return True

    def ask_openai(self, prompt: str) -> None:
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "OpenAi assistant"},
                    {"role": "user", "content": prompt}
                ],
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Erreur OpenAi: {e}")
            return None