import httpx
from sqlalchemy.orm import Session
from typing import Dict
from app import models, oauthDbConfig

class NotionHandler:
    def __init__(self):
        self.service_name = "notion"
        self.api_base = "https://api.notion.com/v1"
    
    def get_auth(self, user_id: int, db: Session):
        user_token = oauthDbConfig.OauthDbConfig.get_user(db, user_id, self.service_name)
        if user_token and user_token.access_token:
            return {"access_token": user_token.access_token}
        return None
    
    def check_action(self, action: models.Action, user_id: int, db: Session) -> bool:
        auth = self.get_auth(user_id, db)
        if not auth:
            return False
        
        if action.name == "new_page_created":
            return self.check_new_page(auth, user_id, db, action)
        
        return False
    
    def check_new_page(self, auth: Dict, user_id: int, db: Session, action: models.Action) -> bool:
        areas = db.query(models.Area).filter_by(user_id=user_id, action_id=action.id).all()
        if not areas:
            return False
        
        headers = {
            "Authorization": f"Bearer {auth['access_token']}",
            "Notion-Version": "2022-06-28"
        }
        
        action_detected = False
        
        for area in areas:
            params = area.parameters or {}
            database_id = params.get("database_id")
            
            if not database_id:
                continue
            try:
                response = httpx.post(
                    f"{self.api_base}/databases/{database_id}/query",
                    headers=headers,
                    json={"page_size": 10},
                    timeout=10.0
                )
                if response.status_code != 200:
                    print(f"Notion error: {response.status_code} - {response.text}")
                    continue
                
                pages = response.json().get("results", [])
                current_page_ids = [page["id"] for page in pages]
                
                previous_ids = params.get("previous_page_ids", [])
                
                if not previous_ids:
                    params["previous_page_ids"] = current_page_ids
                    area.parameters = params
                    db.commit()
                    continue
                
                new_ids = [page_id for page_id in current_page_ids if page_id not in previous_ids]
                
                if new_ids:
                    params["previous_page_ids"] = current_page_ids
                    params["new_page_ids"] = new_ids
                    area.parameters = params
                    action_detected = True
                    
            except Exception as e:
                print(f"Notion error: {e}")
                continue
        
        if action_detected:
            db.commit()
            return True
        
        return False
    
    def execute_reaction(self, reaction: models.Reaction, user_id: int, db: Session) -> bool:
        if reaction.name != "create_page":
            return False
        
        auth = self.get_auth(user_id, db)
        if not auth:
            return False
        
        area = db.query(models.Area).filter_by(user_id=user_id, reaction_id=reaction.id).first()
        if not area:
            return False
        
        return self.create_page(auth, area)
    
    def create_page(self, auth: Dict, area) -> bool:
        params = area.parameters or {}
        title = params.get("title", "Nouvelle page")
        content = params.get("content", "")
        database_id = params.get("database_id")
        
        if not database_id:
            return False
        
        headers = {
            "Authorization": f"Bearer {auth['access_token']}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        }
        
        # cosntruction page
        page_data = {
            "parent": {"database_id": database_id},
            "properties": {
                "Name": {
                    "title": [
                        {"text": {"content": title}}
                    ]
                }
            }
        }
        
        try:
            response = httpx.post(
                f"{self.api_base}/pages",
                headers=headers,
                json=page_data,
                timeout=10.0
            )
            
            if response.status_code == 200:
                print(f"Notion page created: {title}")
                return True
            else:
                print(f"Notion error: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"Notion error: {e}")
            return False