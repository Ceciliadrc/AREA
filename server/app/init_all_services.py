from .database import SessionLocal
from . import models 

def init_services():
    db = SessionLocal()

    all_services = [
    {
    "name": "github",
        "display_name": "GitHub",
        "actions": [
            {
                "name": "new_push",
                "description": "New push to a repository"
            }
        ],
        "reactions": [
            {
                "name": "create_issue",
                "description": "Create a new issue"
            }
        ]
    },
    {
    "name": "dropbox",
        "display_name": "Dropbox",
        "actions": [
            {
                "name": "new_file",
                "description": "A new file is added"
            }
        ],
        "reactions": [
            {
                "name": "upload_file",
                "description": "Upload a file"
            }
        ]
    },
    {
    "name": "twitch",
        "display_name": "Twitch",
        "actions": [
            {
                "name": "favorite_streamer_live",
                "description": "Recieve a notification when your favorite streamer live"
            }
        ],
        "reactions": [
            {
                "name": "send_chat_message",
                "description": "Send a message to a Twitch channel"
            }
        ]
    },
    {
    "name": "microsoft",
        "display_name": "Microsoft",
        "actions": [
            {
                "name": "new_email",
                "description": "New email in Outlook"
            },
            {
                "name": "new_file", 
                "description": "New file in OneDrive"
            }
        ],
        "reactions": [
            {
                "name": "send_email",
                "description": "Send email via Outlook"
            },
            {
                "name": "upload_file",
                "description": "Upload file to OneDrive"
            }
        ]
    },
    {
    "name": "notion",
        "display_name": "Notion",
        "actions": [
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
