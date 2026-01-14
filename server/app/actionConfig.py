ACTION_CONFIGS = {
    "spotify": {
        "user_has_created_new_playlist": {
            "fields": []
        }
    },
    "instagram": {
        "receive_message_from": {
            "fields": [
                {
                    "name": "from_username",
                    "type": "text",
                    "label": "Nom d'utilisateur Instagram",
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
                    "label": "Nom du streamer",
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
                }
            ]
        },
        "upload_file": {
            "fields": [
                {
                    "name": "file_url",
                    "type": "url",
                    "label": "URL du fichier",
                }
            ]
        }
    },
    "notion": {
        "user_mentioned": {
            "fields": []
        },
        "new_page_created": {
            "fields": [
                {
                    "name": "database_id",
                    "type": "text",
                    "label": "ID de la base de données",
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
                }
            ]
        },
    }
}

REACTION_CONFIGS = {
    "spotify": {
        "add_track_to_playlist": {
            "fields": [
                {
                    "name": "playlist_id",
                    "type": "text",
                    "label": "ID de la playlist Spotify"
                },
                {
                    "name": "track_name",
                    "type": "text",
                    "label": "Nom de la musique"
                },
                {
                    "name": "artist",
                    "type": "text",
                    "label": "Artiste"
                }
            ]
        },
        "create_playlist": {
            "fields": [
                {
                    "name": "playlist_name",
                    "type": "text",
                    "label": "Nom de la nouvelle playlist"
                }
            ]
        }
    },
    "instagram": {
        "send_message_to": {
            "fields": [
                {
                    "name": "to_username",
                    "type": "text",
                    "label": "Destinataire"
                },
                {
                    "name": "message",
                    "type": "textarea"
                }
            ]
        }
    },
    "twitch": {
        "suggest_random_stream": {
            "fields": []
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
                    "label": "Contenu"
                },
                {
                    "name": "database_id",
                    "type": "text",
                    "label": "ID de la base de données"
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
                    "label": "Destinataire"
                },
                {
                    "name": "subject",
                    "type": "text",
                    "label": "Sujet"
                },
                {
                    "name": "body",
                    "type": "textarea",
                    "label": "Message"
                }
            ]
        }
    }
}