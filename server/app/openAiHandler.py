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

        auth = self.get_auth(user_id, db)
        if not auth:
            return False

        if action.name == "ask_question":
            return self.ask_question(auth, user_id, db, action)
        elif action.name == "upload_file":
            return self.upload_file(auth, user_id, db, action)
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

    def upload_file(self, auth: Dict, user_id: int, db: Session, action: models.Action) -> bool:
        areas = db.query(models.Area).filter_by(user_id=user_id, action_id=action.id).all()
        if not areas:
            return False

        action_detected = False
        for area in areas:
            params = area.parameters or {}
            file_url = params.get("file_url")
            processed = params.get("processed", False)
            if file_url and not processed:
                params["uploaded_at"] = datetime.now().isoformat()
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

        if reaction.name == "get_answer":
            return self.get_answer(area, db)
        elif reaction.name == "process_file":
            return self.process_file(area, db)

        return False

    def get_answer(self, area, db) -> bool:
        params = area.parameters or {}
        question = params.get("question")
        if not question:
            return False

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "OpenAi assistant"},
                    {"role": "user", "content": question}
                ],
            )
            answer = response.choices[0].message.content
            params["answer"] = answer
            params["answered"] = True
            params["answered_at"] = datetime.now().isoformat()
            area.parameters = params
            db.commit()
            return True

        except Exception as e:
            print(f"Error OpenAi: {e}")
            return False

    def process_file(self, area, db) -> bool:
        params = area.parameters or {}
        file_url = params.get("file_url")
        action_type = params.get("action", "summarize")
        if not file_url:
            return False

        try:
            with httpx.Client() as http_client:
                file = http_client.get(file_url, timeout=30.0)
                if file.status_code != 200:
                    return False

                content = file.headers.get('content-type', '')
                if 'text/' not in content and 'application/json' not in content:
                    params["result"] = f"Upload a .txt, .json or csv file"
                else:
                    file_text = file.text[:2000]
                    prompt = f"{action_type}:\n{file_text}"

            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "OpenAi assistant"},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=300
                )
                result = response.choices[0].message.content
            except Exception as e:
                print(f"Error OpenAi file content: {e}")
                result = e
            params["result"] = result

            params["processed"] = True
            params["processed_at"] = datetime.now().isoformat()
            area.parameters = params
            db.commit()
            return True

        except Exception as e:
            print(f"Error OpenAi: {e}")
            return False
