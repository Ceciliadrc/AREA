import httpx
from sqlalchemy.orm import Session
from datetime import datetime
from app import models, oauthDbConfig

class GithubHandler:
    def __init__(self):
        self.service_name = "github"
        self.api_base = "https://api.github.com"
    
    def get_auth(self, user_id: int, db: Session):
        user_token = oauthDbConfig.OauthDbConfig.get_user(db, user_id, self.service_name)
        if user_token and user_token.access_token:
            return {"access_token": user_token.access_token}
        return None
    
    def check_action(self, action: models.Action, user_id: int, db: Session) -> bool:
        auth = self.get_auth(user_id, db)
        if not auth:
            return False
        
        if action.name == "new_push":
            return self.check_new_push(auth, user_id, db, action)
        
        return False
    
    def check_new_push(self, auth: dict, user_id: int, db: Session, action: models.Action) -> bool:
        areas = db.query(models.Area).filter_by(user_id=user_id, action_id=action.id).all()
        if not areas:
            return False
        
        headers = {
            "Authorization": f"Bearer {auth['access_token']}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        action_detected = False
        
        for area in areas:
            params = area.parameters or {}
            repo = params.get("repository")
            
            if not repo:
                continue
            
            try:
                response = httpx.get(
                    f"{self.api_base}/repos/{repo}/commits",
                    headers=headers,
                    params={"per_page": 5},
                    timeout=10.0
                )
                
                if response.status_code != 200:
                    continue
                
                commits = response.json()
                if not commits:
                    continue
                
                latest_commit_date = commits[0]["commit"]["author"]["date"]
                last_check_date = params.get("last_check_date")
                
                if not last_check_date:
                    params["last_check_date"] = latest_commit_date
                    area.parameters = params
                    db.commit()
                    continue
                
                if latest_commit_date > last_check_date:
                    params["last_check_date"] = latest_commit_date
                    area.parameters = params
                    action_detected = True
                    
            except Exception as e:
                print(f"GitHub error: {e}")
                continue
        
        if action_detected:
            db.commit()
            return True
        
        return False
    
    def execute_reaction(self, reaction: models.Reaction, user_id: int, db: Session) -> bool:
        auth = self.get_auth(user_id, db)
        if not auth:
            return False
        
        if reaction.name == "create_issue":
            return self.create_issue(auth, user_id, db, reaction)
        elif reaction.name == "add_comment":
            return self.add_comment(auth, user_id, db, reaction)
        
        return False
    
    def create_issue(self, auth: dict, user_id: int, db: Session, reaction: models.Reaction) -> bool:
        area = db.query(models.Area).filter_by(user_id=user_id, reaction_id=reaction.id).first()
        if not area:
            return False
        
        params = area.parameters or {}
        repo = params.get("repository")
        title = params.get("title", "Issue from automation")
        body = params.get("body", "Created automatically")
        
        if not repo or not title:
            return False
        
        headers = {
            "Authorization": f"Bearer {auth['access_token']}",
            "Accept": "application/vnd.github.v3+json",
            "Content-Type": "application/json"
        }
        
        try:
            response = httpx.post(
                f"{self.api_base}/repos/{repo}/issues",
                headers=headers,
                json={"title": title, "body": body},
                timeout=10.0
            )
            
            if response.status_code == 201:
                print(f"GitHub issue created")
                return True
            else:
                print(f"GitHub error: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"GitHub error: {e}")
            return False
    
    def add_comment(self, auth: dict, user_id: int, db: Session, reaction: models.Reaction) -> bool:
        area = db.query(models.Area).filter_by(user_id=user_id, reaction_id=reaction.id).first()
        if not area:
            return False
        
        params = area.parameters or {}
        repo = params.get("repository")
        issue_number = params.get("issue_number")
        comment = params.get("comment", "Comment from automation")
        
        if not repo or not issue_number:
            return False
        
        headers = {
            "Authorization": f"Bearer {auth['access_token']}",
            "Accept": "application/vnd.github.v3+json",
            "Content-Type": "application/json"
        }
        
        try:
            response = httpx.post(
                f"{self.api_base}/repos/{repo}/issues/{issue_number}/comments",
                headers=headers,
                json={"body": comment},
                timeout=10.0
            )
            
            if response.status_code == 201:
                print(f"GitHub comment added to issue #{issue_number}")
                return True
            else:
                print(f"GitHub error: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"GitHub error: {e}")
            return False