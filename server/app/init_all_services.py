from .database import SessionLocal
from . import models 

def init_services():
    db = SessionLocal()
    
    all_services = [
        {
            "name": "spotify",
            "display_name": "Spotify",
            "actions": ["user_has_created_new_playlist"],
            "reactions": ["add_track_to_playlist", "create_playlist"]
        },
        {
            "name": "instagram",
            "display_name": "Instagram",
            "actions": ["receive_message_from"],
            "reactions": ["send_message_to"]
        },
        {
            "name": "twitch",
            "display_name": "Twitch",
            "actions": ["favorite_streamer_live"],
            "reactions": ["suggest_random_stream"]
        },
        {
            "name": "openai",
            "display_name": "OpenAI",
            "actions": ["ask_question", "upload_file"],
            "reactions": ["get_answer", "process_file"]
        },
        {
            "name": "notion",
            "display_name": "Notion",
            "actions": ["user_mentioned", "new_page_created"],
            "reactions": ["create_page"]
        },
        {
            "name": "google",
            "display_name": "Gmail",
            "actions": ["new_email", "important_email"],
            "reactions": ["send_email"]
        }
    ]
    created = 0
    for config in all_services:
        service_name = config["name"]
        display_name = config["display_name"]
        
        existing = db.query(models.Service).filter_by(name=service_name).first()
        if existing:
            continue
        
        # cree service
        service = models.Service(name=service_name, display_name=display_name)
        db.add(service)
        db.flush()
        
        # cree action
        for action_name in config["actions"]:
            action = models.Action(service_id=service.id, name=action_name)
            db.add(action)
        
        # cree reaction
        for reaction_name in config["reactions"]:
            reaction = models.Reaction(
                service_id=service.id,
                name=reaction_name
            )
            db.add(reaction)
        
        created += 1
    
    db.commit()
    db.close()
    
    if created > 0:
        print(f"services cree")
    else:
        print("services deja cree")
