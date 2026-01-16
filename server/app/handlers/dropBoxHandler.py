import httpx
import json
from sqlalchemy.orm import Session
from app import models, oauthDbConfig

class DropboxHandler:
    def __init__(self):
        self.service_name = "dropbox"
        self.api_base = "https://api.dropboxapi.com/2"
    
    def get_auth(self, user_id: int, db: Session):
        user_token = oauthDbConfig.OauthDbConfig.get_user(db, user_id, self.service_name)
        if user_token and user_token.access_token:
            return {"access_token": user_token.access_token}
        return None
    
    def check_action(self, action: models.Action, user_id: int, db: Session) -> bool:
        if action.name != "new_file":
            return False
        
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
            folder_path = params.get("folder_path")
            
            if not folder_path:
                continue
            
            try:
                response = httpx.post(
                    f"{self.api_base}/files/list_folder",
                    headers=headers,
                    json={"path": folder_path, "limit": 50},
                    timeout=10.0
                )
                
                if response.status_code != 200:
                    continue
                
                current_files = response.json().get("entries", [])
                current_ids = [f["id"] for f in current_files if f[".tag"] == "file"]
                
                previous_ids = params.get("previous_file_ids", [])
                
                if not previous_ids:
                    params["previous_file_ids"] = current_ids
                    area.parameters = params
                    db.commit()
                    continue
                
                new_ids = [file_id for file_id in current_ids if file_id not in previous_ids]
                
                if new_ids:
                    params["detected_files"] = new_ids
                    params["previous_file_ids"] = current_ids
                    area.parameters = params
                    action_detected = True
                    
            except Exception as e:
                print(f"Dropbox error: {e}")
                continue
        
        if action_detected:
            db.commit()
            return True
        
        return False
    
    def execute_reaction(self, reaction: models.Reaction, user_id: int, db: Session) -> bool:
        if reaction.name != "upload_file":
            return False
        
        auth = self.get_auth(user_id, db)
        if not auth:
            return False
        
        area = db.query(models.Area).filter_by(user_id=user_id, reaction_id=reaction.id).first()
        if not area:
            return False
        
        params = area.parameters or {}
        file_path = params.get("file_path")
        content = params.get("content", "")
        
        if not file_path:
            return False
        
        try:
            headers = {
                "Authorization": f"Bearer {auth['access_token']}",
                "Content-Type": "application/octet-stream",
                "Dropbox-API-Arg": json.dumps({
                    "path": file_path,
                    "mode": "overwrite",
                    "autorename": True,
                    "mute": False
                })
            }
            
            response = httpx.post(
                "https://content.dropboxapi.com/2/files/upload",
                headers=headers,
                content=content.encode('utf-8'),
                timeout=10.0
            )
            
            if response.status_code == 200:
                print(f"Dropbox file uploaded")
                return True
                
        except Exception as e:
            print(f"Dropbox error: {e}")
            return False