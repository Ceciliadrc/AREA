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
            oauth_config = db.query(models.ServiceOauth).filter_by(service_id=service.id).first()
            
            if not oauth_config:
                return None
                
            return {
                "access_token": user_token.access_token,
                "refresh_token": user_token.refresh_token,
                "client_id": oauth_config.client_id,
                "user_id": user_id
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
        try:
            areas = db.query(models.Area).filter_by(user_id=user_id, action_id=action.id).all()
            
            if not areas:
                return False
            
            headers = {
                "Authorization": f"Bearer {auth['access_token']}",
                "Client-Id": auth['client_id']
            }
            
            action_detected = False
            
            for area in areas:
                streamer = area.parameters.get("streamer") if area.parameters else "zerator"
                
                with httpx.Client() as client:
                    response = client.get(
                        f"{self.api_base}/streams",
                        headers=headers,
                        params={"user_login": streamer},
                        timeout=10.0
                    )
                    
                    if response.status_code != 200:
                        continue
                    
                    data = response.json().get("data", [])
                    
                    is_live = len(data) > 0

                    if is_live:
                        if area.parameters is None:
                            area.parameters = {}
                        
                        area.parameters["was_live"] = True
                        area.parameters["streamer"] = streamer
                        
                        if data:
                            stream_data = data[0]
                            area.parameters["stream_title"] = stream_data.get("title", "")

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

        if reaction.name == "suggest_random_stream":
            return self.suggest_random_stream(auth)
        
        return False
    
    def suggest_random_stream(self, auth: Dict) -> bool:
        try:
            headers = {
                "Authorization": f"Bearer {auth['access_token']}",
                "Client-Id": auth['client_id']
            }
            
            with httpx.Client() as client:
                response = client.get(
                    f"{self.api_base}/streams",
                    headers=headers,
                    params={
                        "first": 10,
                        "language": "fr"
                    },
                    timeout=10.0
                )
                
                if response.status_code != 200:
                    return False
                
                streams = response.json().get("data", [])

        except Exception:
            return False
