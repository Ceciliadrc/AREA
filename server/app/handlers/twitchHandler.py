import httpx
from sqlalchemy.orm import Session
from typing import Dict
from app import models, oauthDbConfig

class TwitchHandler:
    def __init__(self):
        self.service_name = "twitch"
        self.api_base = "https://api.twitch.tv/helix"
    
    def get_auth(self, user_id: int, db: Session):
        user_token = oauthDbConfig.OauthDbConfig.get_user(db, user_id, self.service_name)
        
        if user_token and user_token.access_token:
            service = db.query(models.Service).filter_by(name=self.service_name).first()
            if service and service.oauth_config:
                return {
                    "access_token": user_token.access_token,
                    "client_id": service.oauth_config.client_id,
                    "twitch_user_id": user_token.provider_user_id
                }
        return None
    
    def check_action(self, action: models.Action, user_id: int, db: Session) -> bool:
        auth = self.get_auth(user_id, db)
        if not auth:
            return False
        
        if action.name == "favorite_streamer_live":
            return self.check_streamer_live(auth, user_id, db, action)
        
        return False
    
    def check_streamer_live(self, auth: Dict, user_id: int, db: Session, action: models.Action) -> bool:
        areas = db.query(models.Area).filter_by(user_id=user_id, action_id=action.id).all()
        if not areas:
            return False
        
        headers = {
            "Authorization": f"Bearer {auth['access_token']}",
            "Client-Id": auth['client_id']
        }
        
        action_detected = False
        
        for area in areas:
            params = area.parameters or {}
            streamer = params.get("streamer_name")
            
            try:
                response = httpx.get(
                    f"{self.api_base}/streams",
                    headers=headers,
                    params={"user_login": streamer},
                    timeout=10.0
                )
                if response.status_code != 200:
                    continue
                
                data = response.json().get("data", [])
                is_live = len(data) > 0
                
                was_live = params.get("was_live", False)
                
                if is_live and not was_live:
                    params["was_live"] = True
                    if data:
                        stream_data = data[0]
                        params["stream_title"] = stream_data.get("title", "")
                    
                    area.parameters = params
                    action_detected = True
            except Exception as e:
                print(f"Twitch error: {e}")
                continue
        
        if action_detected:
            db.commit()
            return True
        
        return False
    
    def execute_reaction(self, reaction: models.Reaction, user_id: int, db: Session) -> bool:
        auth = self.get_auth(user_id, db)
        if not auth:
            return False
        
        if reaction.name != "send_chat_message":
            return False
        
        return self.send_chat_message(auth, user_id, db, reaction)
        
    def send_chat_message(self, auth: Dict, user_id: int, db: Session, reaction: models.Reaction) -> bool:
        area = db.query(models.Area).filter_by(user_id=user_id, reaction_id=reaction.id).first()
        if not area:
            return False
        
        params = area.parameters or {}
        channel = params.get("channel", "").lower().strip().lstrip('#')
        message = params.get("message", "").strip()
        
        if not channel or not message or len(message) > 500:
            return False
        
        headers = {
            "Authorization": f"Bearer {auth['access_token']}",
            "Client-Id": auth['client_id']
        }
        
        #  recuepre id de la chaine
        try:
            user_resp = httpx.get(
                f"{self.api_base}/users",
                headers=headers,
                params={"login": channel},
                timeout=10.0
            )
            if user_resp.status_code != 200:
                return False
            broadcaster_id = user_resp.json()["data"][0]["id"]
        except:
            return False

        moderator_id = auth.get("twitch_user_id")
        if not moderator_id:
            return False
        
        try:
            chat_resp = httpx.post(
                f"{self.api_base}/chat/messages",
                headers=headers,
                json={
                    "broadcaster_id": broadcaster_id,
                    "moderator_id": moderator_id,
                    "message": message
                },
                timeout=10.0
            )
            return chat_resp.status_code == 200
        except:
            return False