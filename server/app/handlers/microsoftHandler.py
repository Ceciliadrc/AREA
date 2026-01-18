import httpx
from sqlalchemy.orm import Session
from typing import Dict
from app import models, oauthDbConfig
import json

class MicrosoftHandler:
    def __init__(self):
        self.service_name = "microsoft"
        self.api_base = "https://graph.microsoft.com/v1.0"
    
    def get_auth(self, user_id: int, db: Session):
        user_token = oauthDbConfig.OauthDbConfig.get_user(db, user_id, self.service_name)
        if user_token and user_token.access_token:
            return {"access_token": user_token.access_token}
        return None
    
    def check_action(self, action: models.Action, user_id: int, db: Session) -> bool:
        auth = self.get_auth(user_id, db)
        if not auth:
            return False
        
        areas = db.query(models.Area).filter_by(user_id=user_id, action_id=action.id).all()
        if not areas:
            return False
        
        headers = {"Authorization": f"Bearer {auth['access_token']}"}
        action_detected = False
        
        for area in areas:
            params = area.parameters or {}
            
            if action.name == "new_email":
                return self.check_microsoft_email(headers, area, params, db)
            elif action.name == "new_file":
                return self.check_microsoft_file(headers, area, params, db)
        if action_detected:
            db.commit()
            return True
        
        return False
    
    def check_microsoft_email(self, headers: Dict, area: models.Area, params: Dict, db: Session) -> bool:
        filter_parts = []
        
        if params.get("sender"):
            filter_parts.append(f"from/emailAddress/address eq '{params['sender']}'")
        
        if params.get("subject_contains"):
            filter_parts.append(f"contains(subject, '{params['subject_contains']}')")
        
        filter_query = " and ".join(filter_parts)
        
        response = httpx.get(
            f"{self.api_base}/me/messages",
            headers=headers,
            params={
                "$filter": filter_query,
                "$top": 10,
                "$orderby": "receivedDateTime desc"
            },
            timeout=10.0
        )
        if response.status_code != 200:
            return False
        
        messages = response.json().get("value", [])
        current_message_ids = [msg["id"] for msg in messages]
        
        previous_ids = params.get("previous_emails", [])
        
        if not previous_ids:
            params["previous_emails"] = current_message_ids
            area.parameters = params
            return False
        
        new_ids = [msg_id for msg_id in current_message_ids if msg_id not in previous_ids]
        
        if new_ids:
            params["previous_emails"] = current_message_ids
            params["new_email_ids"] = new_ids
            area.parameters = params
            return True  
        return False

    def check_microsoft_file(self, headers: Dict, area: models.Area, params: Dict, db: Session) -> bool:
        folder_path = params.get("folder", "/")
        
        response = httpx.get(
            f"{self.api_base}/me/drive/root:{folder_path}/children",
            headers=headers,
            params={
                "$top": 10,
                "$orderby": "createdDateTime desc"
            },
            timeout=10.0
        )
        
        if response.status_code != 200:
            return False
        
        files = response.json().get("value", [])
        current_file_ids = [file["id"] for file in files]

        previous_ids = params.get("previous_files", [])

        if not previous_ids:
            params["previous_files"] = current_file_ids
            area.parameters = params
            return False
        
        new_ids = [file_id for file_id in current_file_ids if file_id not in previous_ids]
        
        if new_ids:
            params["previous_files"] = current_file_ids
            params["new_file_ids"] = new_ids
            area.parameters = params
            return True
        
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
            return self.send_outlook_email(auth, params)
        elif reaction.name == "upload_file":
            return self.upload_onedrive_file(auth, params)
        
        return False
    
    def send_outlook_email(self, auth: Dict, params) -> bool:
        if isinstance(params, str):
            params = json.loads(params)
        
        if not isinstance(params, dict):
            return False
        
        to_email = params.get("to")
        subject = params.get("subject", "")
        message = params.get("message", "")
        
        if not to_email:
            return False
        
        email_data = {
            "message": {
                "subject": subject,
                "body": {
                    "contentType": "Text",
                    "content": message
                },
                "toRecipients": [
                    {
                        "emailAddress": {
                            "address": to_email
                        }
                    }
                ]
            },
            "saveToSentItems": True
        }
        headers = {
            "Authorization": f"Bearer {auth['access_token']}",
            "Content-Type": "application/json"
        }
        response = httpx.post(
            f"{self.api_base}/me/sendMail",
            headers=headers,
            json=email_data,
            timeout=10.0
        )
        return response.status_code == 202
    
    def upload_onedrive_file(self, auth: Dict, params: Dict) -> bool:
        file_path = params.get("path", "")
        content = params.get("content", "")
        
        if not content:
            return False
        
        headers = {
            "Authorization": f"Bearer {auth['access_token']}",
            "Content-Type": "text/plain"
        }
        response = httpx.put(
            f"{self.api_base}/me/drive/root:{file_path}/content",
            headers=headers,
            content=content,
            timeout=10.0
        )
        return response.status_code in [200, 201]
