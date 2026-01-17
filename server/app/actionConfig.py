ACTION_CONFIGS = {
    "github": {
        "new_push": {
            "fields": [
                {
                    "name": "repository",
                    "type": "text",
                    "label": "Repository (format: owner/repo)",
                    "required": True
                }
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
                    "label": "Twitch streamer name",
                    "required": True
                }
            ]
        }
    },
    "microsoft": {
        "new_email": {
            "fields": [
                {
                    "name": "sender",
                    "type": "email",
                    "required": False
                }
            ]
        },
        "new_file": {
            "fields": [
                {
                    "name": "folder",
                    "type": "text", 
                    "label": "Folder path",
                    "required": True,
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
                    "label": "Database ID",
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
                    "label": "Specific sender",
                    "required": False
                },
                {
                    "name": "subject_contains",
                    "type": "text",
                    "label": "Subject contains",
                    "required": False
                }
            ]
        },
        "important_email": {
            "fields": [
                {
                    "name": "from_email",
                    "type": "email",
                    "label": "Specific sender",
                    "required": False
                }
            ]
        }
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
                    "required": False
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
                    "required": True
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
                    "label": "Twitch channel",
                    "required": True
                },
                {
                    "name": "message", 
                    "type": "textarea",
                    "label": "Message to send",
                    "required": True
                }
            ]
        }
    },
    "microsoft": {
        "send_email": {
            "fields": [
                {
                    "name": "to",
                    "type": "email",
                    "label": "To",
                    "required": True
                },
                {
                    "name": "subject", 
                    "type": "text",
                    "label": "Subject",
                    "required": True
                },
                {
                    "name": "message",
                    "type": "textarea",
                    "label": "Message",
                    "required": True
                }
            ]
        },
        "upload_file": {
            "fields": [
                {
                    "name": "path",
                    "type": "text",
                    "label": "File path",
                    "required": True,
                },
                {
                    "name": "content",
                    "type": "textarea", 
                    "label": "Content",
                    "required": True
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
                    "label": "Page title",
                    "required": True
                },
                {
                    "name": "content",
                    "type": "textarea",
                    "label": "Content",
                    "required": False
                },
                {
                    "name": "database_id",
                    "type": "text",
                    "label": "Database ID",
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
                    "label": "Recipient",
                    "required": True
                },
                {
                    "name": "subject",
                    "type": "text",
                    "label": "Subject",
                    "required": True
                },
                {
                    "name": "body",
                    "type": "textarea",
                    "label": "Message",
                    "required": True
                }
            ]
        }
    }
}