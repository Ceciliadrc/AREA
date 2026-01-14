##
## EPITECH PROJECT, 2026
## AREA
## File description:
## intagramHandler
##

import httpx
from sqlalchemy.orm import Session
from app import models, oauthDbConfig
from typing import Dict

class InstagramHandler:
    def __init__(self):
        self.service_name = "instagram"
        self.api_base = "https://graph.instagram.com/"

    def get_auth(self, user_id: int, db: Session):
        user_token = oauthDbConfig.OauthDbConfig.get_user(db, user_id, self.service_name)

        if user_token and user_token.access_token:
            return {"access_token": user_token.access_token, "user_id": user_id}
        return None

    def check_action(self, action: models.Action, user_id:int, db: Session) -> bool:
        auth = self.get_auth(user_id, db)

        if not auth:
            return False

        if action.name == "receive_message_from":
            return self.receive_message_from(auth, user_id, db, action)

        return False

    def receive_message_from(self, auth: Dict, user_id: int, db: Session, action: models.Action) -> bool:
        try:
            headers = {"Authorization": f"Bearer {auth['access_token']}"}

            with httpx.Client() as client:
                response = client.get(f"{self.api_base}/me/conversations", headers=headers)
                if response.status_code != 200:
                    return False

                conversations = response.json().get("data", [])
                current_ids = [conv["id"] for conv in conversations]

            areas = db.query(models.Area).filter_by(user_id=user_id, action_id=action.id).all()

            if not areas:
                return False

            action_detected = False

            for area in areas:
                if area.parameters is None:
                    area.parameters = {}

                previous_ids = area.parameters.get("previous_ids", []) if area.parameters else []

                new_ids = [cid for cid in current_ids if cid not in previous_ids]

                if new_ids:
                    area.parameters["new_ids"] = new_ids
                    action_detected = True

                area.parameters["previous_ids"] = current_ids

            db.commit()
            return action_detected

        except Exception as e:
            print(f"Error: {e}")
            return False

    def execute_reaction(self, reaction: models.Reaction, user_id: int, db: Session) -> bool:
        auth = self.get_auth(user_id, db)
        if not auth:
            return False
        area = db.query(models.Area).filter_by(user_id=user_id, reaction_id=reaction.id).first()

        if not area:
            return False

        parameters = area.parameters or {}

        if reaction.name == "send_message_to":
            return self.send_message_to(auth, parameters)

        return False

    def send_message_to(self, auth: Dict, parameters: Dict):
        try:
            headers = {"Authorization": f"Bearer {auth['access_token']}"}

            recipient_id = parameters.get("recipient_id")
            message_id = parameters.get("message_id")

            if not recipient_id or not message_id:
                return False

            data = {
                "recipient": {"id": recipient_id},
                "message": {"text": message_id},
            }

            with httpx.Client() as client:
                response = client.post("https://graph.facebook.com/v17.0/me/messages", headers=headers, json=data, timeout=10.0)
                return response.status_code in [200, 201]

        except Exception as e:
            print(f"Error: {e}")
            return False
