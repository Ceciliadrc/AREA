import time
import threading
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models

from .handlers.gmailHandler import GmailHandler
from .handlers.notionHandler import NotionHandler
from .handlers.twitchHandler import TwitchHandler
from .handlers.githubHandler import GithubHandler
from .handlers.dropBoxHandler import DropboxHandler
# from .handlers.microsoftHandler import MicrosoftHandler

class Hook:
    def __init__(self):
        self.running = False
        self.thread = None

        self.handlers = {
            "google": GmailHandler(),
            "notion": NotionHandler(),
            "twitch": TwitchHandler(),
            "github": GithubHandler(),
            "dropbox": DropboxHandler(),
            # "microsoft": MicrosoftHandler(),
        }
    def get_handler(self, service_name: str):
        return self.handlers.get(service_name)
    
    def get_area(self):
        db = SessionLocal()
        areas = db.query(models.Area).all()
            
        if not areas:
            db.close()
            return  
        for area in areas:
            self.process_single_area(area, db)    
        db.close()
    
    def process_single_area(self, area: models.Area, db: Session):
        action = db.query(models.Action).filter_by(id=area.action_id).first()
        if not action:
            return

        service = db.query(models.Service).filter_by(id=action.service_id).first()
        if not service:
            return
            
        handler = self.get_handler(service.name)
        if not handler:
            return
            
        action_happened = handler.check_action(action, area.user_id, db)
            
        if action_happened:
            reaction = db.query(models.Reaction).filter_by(id=area.reaction_id).first()
            if not reaction:
                return
            handler.execute_reaction(reaction, area.user_id, db)
    
    def run(self):
        while self.running:
            self.get_area()
            time.sleep(60)

    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self.run, daemon=True)
            self.thread.start()

hook = Hook()
