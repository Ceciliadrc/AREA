from .database import SessionLocal
from . import models 

def init_services():
    db = SessionLocal()

    all_services = [
        {
            "name": "spotify",
            "display_name": "Spotify",
            "actions": [
                {
                    "name": "user_has_created_new_playlist",
                    "description": "Check if a new playlist is created by the user"
                }
            ],
            "reactions": [
                {
                    "name": "add_track_to_playlist",
                    "description": "Add a track to a playlist"
                },
                {
                    "name": "create_playlist",
                    "description": "Create a new playlist"
                }
            ]
        },
        {
            "name": "instagram",
            "display_name": "Instagram",
            "actions": [
                {
                    "name": "receive_message_from",
                    "description": "Receive a message from a specific user"
                }
            ],
            "reactions": [
                {
                    "name": "send_message_to",
                    "description": "Send a message to a specific user"
                }
            ]
        },
        {
            "name": "twitch",
            "display_name": "Twitch",
            "actions": [
                {
                    "name": "favorite_streamer_live",
                    "description": "Recieve a notification when your favoritte streamer live"
                }
            ],
            "reactions": [
                {
                    "name": "suggest_random_stream",
                    "description": "Suggest a live stream to watch"
                }
            ]
        },
        {
            "name": "openai",
            "display_name": "OpenAI",
            "actions": [
                {
                    "name": "ask_question",
                    "description": "Ask a question to the AI"
                },
                {
                    "name": "upload_file",
                    "description": "Upload a file for processing"
                }
            ],
            "reactions": [
                {
                    "name": "get_answer",
                    "description": "Get an answer from the AI"
                },
                {
                    "name": "process_file",
                    "description": "Process an uploaded file"
                }
            ]
        },
        {
            "name": "notion",
            "display_name": "Notion",
            "actions": [
                {
                    "name": "user_mentioned",
                    "description": "Get mentioned in a Notion page"
                },
                {
                    "name": "new_page_created",
                    "description": "A new page is created in your workspace"
                }
            ],
            "reactions": [
                {
                    "name": "create_page",
                    "description": "Create a new page in Notion"
                }
            ]
        },
        {
            "name": "google",
            "display_name": "Gmail",
            "actions": [
                {
                    "name": "new_email",
                    "description": "Receive a new email"
                },
                {
                    "name": "important_email",
                    "description": "Receive an important email"
                }
            ],
            "reactions": [
                {
                    "name": "send_email",
                    "description": "Send an email to a recipient"
                }
            ]
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
        for action_config in config["actions"]:
            action = models.Action(service_id=service.id, name=action_config["name"], description=action_config["description"])
            db.add(action)
        
        # cree reaction
        for reaction_config in config["reactions"]:
            reaction = models.Reaction(service_id=service.id,name=reaction_config["name"], description=reaction_config["description"])
            db.add(reaction)

        created += 1
    
    db.commit()
    db.close()
    
    if created > 0:
        print(f"services cree")
    else:
        print("services deja cree")
