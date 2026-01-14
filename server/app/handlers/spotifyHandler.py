import httpx
from sqlalchemy.orm import Session
from app import models, oauthDbConfig
from typing import Dict

class SpotifyHandler:
    def __init__(self):
        self.service_name = "spotify"
        self.api_base = "https://api.spotify.com/v1"

    def get_auth(self, user_id: int, db: Session):
        user_token = oauthDbConfig.OauthDbConfig.get_user(db, user_id, self.service_name)
        
        if user_token and user_token.access_token:
            return {
                "access_token": user_token.access_token,
                "refresh_token": user_token.refresh_token,
                "user_id": user_id
            }
        return None
    
    def check_action(self, action: models.Action, user_id: int, db: Session):
        if action.name != "user_has_created_new_playlist":
            return False
            
        auth = self.get_auth(user_id, db)
        if not auth:
            return False
        
        return self.detect_new_playlist(auth, user_id, db, action)
    
    def detect_new_playlist(self, auth: Dict, user_id: int, db: Session, action: models.Action) -> bool:
        try:
            headers = {"Authorization": f"Bearer {auth['access_token']}"}
            
            with httpx.Client() as client:
                response = client.get(f"{self.api_base}/me/playlists", headers=headers)
                if response.status_code != 200:
                    return False
                
                playlists = response.json().get("items", [])
                current_ids = [p["id"] for p in playlists]  # Liste des IDs actuels
            
            # Trouve l'AREA pour cet utilisateur
            area = db.query(models.Area).filter_by(
                user_id=user_id, 
                action_id=action.id
            ).first()
            
            if not area:
                return False
            
            # Récupère les IDs précédents
            params = area.parameters or {}
            previous_ids = params.get("previous_playlist_ids", [])
            
            # Trouve les NOUVEAUX IDs
            new_ids = [pid for pid in current_ids if pid not in previous_ids]
            
            if new_ids:
                params["previous_playlist_ids"] = current_ids
                params["new_playlist_ids"] = new_ids
                area.parameters = params
                
                db.commit()
                return True

            params["previous_playlist_ids"] = current_ids
            area.parameters = params
            db.commit()
            
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
        
        if reaction.name == "add_track_to_playlist":
            playlist_id = params.get("playlist_id")
            track_name = params.get("track_name")
            
            if not playlist_id or not track_name:
                return False
            
            # Recherche la musique
            track_uri = self.search_track(auth, track_name, params.get("artist", ""))
            if not track_uri:
                return False
            
            return self.add_track(auth, playlist_id, track_uri)
        
        elif reaction.name == "create_playlist":
            playlist_name = params.get("playlist_name", "AREA Playlist")
            return self.create_playlist(auth, playlist_name)
        
        return False
    
    def search_track(self, auth: Dict, track_name: str, artist: str = "") -> str:
        try:
            headers = {"Authorization": f"Bearer {auth['access_token']}"}
            query = f"track:{track_name}"
            if artist:
                query += f" artist:{artist}"
            
            with httpx.Client() as client:
                response = client.get(
                    f"{self.api_base}/search",
                    headers=headers,
                    params={"q": query, "type": "track", "limit": 1}
                )
                
                if response.status_code == 200:
                    tracks = response.json().get("tracks", {}).get("items", [])
                    if tracks:
                        return tracks[0]["uri"]
            return None
        except Exception:
            return None
    
    def add_track(self, auth: Dict, playlist_id: str, track_uri: str) -> bool:
        try:
            headers = {"Authorization": f"Bearer {auth['access_token']}"}
            data = {"uris": [track_uri]}
            
            with httpx.Client() as client:
                response = client.post(
                    f"{self.api_base}/playlists/{playlist_id}/tracks",
                    headers=headers,
                    json=data
                )
                return response.status_code in [200, 201]
        except Exception:
            return False
    
    def create_playlist(self, auth: Dict, name: str) -> bool:
        try:
            headers = {"Authorization": f"Bearer {auth['access_token']}"}
            
            with httpx.Client() as client:
                user_resp = client.get(f"{self.api_base}/me", headers=headers)
                if user_resp.status_code != 200:
                    return False
                
                user_id = user_resp.json().get("id")
                
                # cree playlist
                data = {"name": name, "public": False}
                response = client.post(
                    f"{self.api_base}/users/{user_id}/playlists",
                    headers=headers,
                    json=data
                )
                return response.status_code == 201
        except Exception:
            return False