import httpx
import base64
from sqlalchemy.orm import Session
from email.mime.text import MIMEText
from typing import Dict
from app import models, oauthDbConfig

class GmailHandler:
    def __init__(self):
        self.service_name = "google"
        self.api_base = "https://gmail.googleapis.com/gmail/v1/users/me"
    
    def get_auth(self, user_id: int, db: Session):
        user_token = oauthDbConfig.OauthDbConfig.get_user(db, user_id, self.service_name)
        
        if user_token and user_token.access_token:
            return {
                "access_token": user_token.access_token,
                "refresh_token": user_token.refresh_token,
                "user_id": user_id
            }
        return None
    
    def check_action(self, action: models.Action, user_id: int, db: Session) -> bool:
        auth = self.get_auth(user_id, db)
        if not auth:
            return False
        
        if action.name == "new_email":
            return self.check_new_email(auth, user_id, db, action)
        return False
    
    def check_new_email(self, auth: Dict, user_id: int, db: Session, action: models.Action) -> bool:
        try:
            areas = db.query(models.Area).filter_by(user_id=user_id, action_id=action.id).all()
            
            if not areas:
                return False
            
            headers = {"Authorization": f"Bearer {auth['access_token']}"}
            
            with httpx.Client() as client:
                response = client.get(
                    f"{self.api_base}/messages",
                    headers=headers,
                    params={"q": "is:unread", "maxResults": 5}
                )
                
                if response.status_code != 200:
                    return False
                
                # recupere la list des gmail
                emails_data = response.json().get("messages", [])
                current_email_ids = [email["id"] for email in emails_data]
            
            action_detected = False
            
            for area in areas:
                previous_ids = area.parameters.get("previous_emails", [])
                
                # compare pour trouver les previous au nouveau
                new_ids = [email_id for email_id in current_email_ids if email_id not in previous_ids]
                
                if new_ids:
                    if area.parameters is None:
                        area.parameters = {}
                    # stoke pour la prochaine verif
                    area.parameters["previous_emails"] = current_email_ids
                    area.parameters["new_email_ids"] = new_ids
                    
                    action_detected = True
            
            if action_detected:
                db.commit()
                return True
            
            return False
            
        except Exception:
            return False
    
    def execute_reaction(self, reaction: models.Reaction, user_id: int, db: Session) -> bool:
        auth = self.get_auth(user_id, db)
        if not auth:
            return False
        
        area = db.query(models.Area).filter_by(user_id=user_id, reaction_id=reaction.id).first()
        
        if not area:
            return False
        
        params = area.parameters or {}
        
        if reaction.name == "send_email":
            to_email = params.get("to")
            subject = params.get("subject", "")
            body = params.get("body", "")
            
            if not to_email:
                return False
            
            return self.send_email(auth, to_email, subject, body)
        
        return False
    
    def send_email(self, auth: Dict, to_email: str, subject: str, body: str) -> bool:
        try:
            message = MIMEText(body)
            message["to"] = to_email
            message["subject"] = subject
            message["from"] = "me"
            
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            
            headers = {"Authorization": f"Bearer {auth['access_token']}"}
            
            with httpx.Client() as client:
                response = client.post(
                    f"{self.api_base}/messages/send",
                    headers=headers,
                    json={"raw": raw_message},
                )
                return response.status_code == 200
                
        except Exception:
            return False
