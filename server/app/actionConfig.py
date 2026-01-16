ACTION_CONFIGS = {
    "github": {
        "new_push": {
            "fields": [
                {
                    "name": "repository",
                    "type": "text",
                    "label": "Repository (format: owner/repo)",
                    "required": True
                },
            ]
        }
    },
    "dropbox": {
        "new_file": {
            "fields": [
                {
                    "name": "folder_path",
                    "type": "text",
                    "label": "Folder to watch",
                    "required": True
                }
            ]
        }
    },
    "twitch": {
        "favorite_streamer_live": {
            "fields": [
                {
                    "name": "streamer_name",
                    "type": "text",
                    "label": "Nom du streamer Twitch",
                    "required": True
                }
            ]
        }
    },
    "openai": {
        "ask_question": {
            "fields": [
                {
                    "name": "question",
                    "type": "textarea",
                    "label": "Question à poser",
                    "required": True
                }
            ]
        },
        "upload_file": {
            "fields": [
                {
                    "name": "file_url",
                    "type": "url",
                    "label": "URL du fichier",
                    "required": True
                }
            ]
        }
    },
    "notion": {
        "new_page_created": {
            "fields": [
                {
                    "name": "database_id",
                    "type": "text",
                    "label": "ID de la base de données",
                    "required": True
                }
            ]
        }
    },
    "google": {
        "new_email": {
            "fields": [
                {
                    "name": "from_email",
                    "type": "email",
                    "label": "Expéditeur spécifique",
                },
                {
                    "name": "subject_contains",
                    "type": "text",
                    "label": "Sujet contient",
                }
            ]
        },
    }
}

REACTION_CONFIGS = {
    "github": {
        "create_issue": {
            "fields": [
                {
                    "name": "repository",
                    "type": "text",
                    "label": "Repository (format: owner/repo)",
                    "required": True
                },
                {
                    "name": "title",
                    "type": "text",
                    "label": "Issue title",
                    "required": True
                },
                {
                    "name": "body",
                    "type": "textarea",
                    "label": "Issue description",
                }
            ]
        }
    },
    "dropbox": {
        "upload_file": {
            "fields": [
                {
                    "name": "file_path",
                    "type": "text",
                    "label": "File path",
                    "required": True
                },
                {
                    "name": "content",
                    "type": "textarea",
                    "label": "File content",
                }
            ]
        }
    },
    "twitch": {
        "send_chat_message": {
            "fields": [
                {
                    "name": "channel",
                    "type": "text",
                    "label": "Channel Twitch",
                    "required": True
                },
                {
                    "name": "message", 
                    "type": "textarea",
                    "label": "Message à envoyer",
                    "required": True
                }
            ]
        }
    },
    "openai": {
        "get_answer": {
            "fields": []
        },
        "process_file": {
            "fields": [
                {
                    "name": "action",
                    "type": "select",
                    "label": "Action à effectuer",
                }
            ]
        }
    },
    "notion": {
        "create_page": {
            "fields": [
                {
                    "name": "title",
                    "type": "text",
                    "label": "Titre de la page",
                    "required": True
                },
                {
                    "name": "content",
                    "type": "textarea",
                    "label": "Contenu",
                },
                {
                    "name": "database_id",
                    "type": "text",
                    "label": "ID de la base de données",
                    "required": True
                }
            ]
        }
    },
    "google": {
        "send_email": {
            "fields": [
                {
                    "name": "to_email",
                    "type": "email",
                    "label": "Destinataire",
                    "required": True
                },
                {
                    "name": "subject",
                    "type": "text",
                    "label": "Sujet",
                    "required": True
                },
                {
                    "name": "body",
                    "type": "textarea",
                    "label": "Message",
                }
            ]
        }
    }
}