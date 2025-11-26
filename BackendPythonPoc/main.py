##
## EPITECH PROJECT, 2025
## AREA
## File description:
## main
##

from fastapi import FastAPI
import time
import json

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "AREA Backend POC - Welcome!"}

@app.get("/about.json")
async def about():
    return {
        "client": {"host": "127.0.0.1"},
        "server": {
            "current_time": int(time.time()),
            "services": [
                {
                    "name": "google",
                    "actions": [
                        {"name": "new_email", "description": "A new email is received"},
                        {"name": "new_calendar_event", "description": "A new event is added to calendar"}
                    ],
                    "reactions": [
                        {"name": "send_email", "description": "Send an email"},
                        {"name": "create_event", "description": "Create a calendar event"}
                    ]
                }
            ]
        }
    }

@app.get("/services")
async def get_services():
    return [
        {
            "name": "google",
            "actions": [
                {"name": "new_email", "description": "A new email is received"},
                {"name": "new_calendar_event", "description": "A new event is added to calendar"}
            ],
            "reactions": [
                {"name": "send_email", "description": "Send an email"},
                {"name": "create_event", "description": "Create a calendar event"}
            ]
        }
    ]

@app.post("/area")
async def create_area(action_service: str, action_name: str, reaction_service: str, reaction_name: str):
    return {
        "message": "AREA created successfully",
        "area": {
            "action": f"{action_service}.{action_name}",
            "reaction": f"{reaction_service}.{reaction_name}"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)