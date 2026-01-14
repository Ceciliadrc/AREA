from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import time
from app import models, database
from sqlalchemy.orm import Session
from .auth import router as auth_router
from .areas import router as areas_router
from .services import router as services_router
from sqlalchemy import exc
# from app.hook import hook
from .authSpotify import router as spotify_auth_router
# from .authGoogle import router as google_auth_router
# from .authTwitch import router as twitch_auth_router
# from .authNotion import router as notion_auth_router
# from .authInsta import router as insta_auth_router
from .init_all_services import init_services

def wait_for_db():
    for _ in range(10):
        try:
            database.engine.connect()
            return True
        except exc.OperationalError:
            time.sleep(1)
    return False

if wait_for_db():
   models.Base.metadata.create_all(bind=database.engine)
   init_services()
    # hook.start()
    # print("hook démarré")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8081",
        "http://127.0.0.1:8081",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(areas_router)
app.include_router(services_router)
app.include_router(spotify_auth_router)
# app.include_router(google_auth_router)
# app.include_router(twitch_auth_router)
# app.include_router(notion_auth_router)
# app.include_router(insta_auth_router)

@app.get("/")
async def root():
    return {"message": "API is working"}

@app.get("/about.json")
async def about(db: Session = Depends(database.get_db)):

    services_data = []
    services = db.query(models.Service).all()

    for service in services:
        actions = db.query(models.Action).filter(models.Action.service_id == service.id).all()
        reactions = db.query(models.Reaction).filter(models.Reaction.service_id == service.id).all()
    
        services_data.append({
                "name": service.name,
                "actions": [
                    {"name": action.name}
                    for action in actions
                ],
                "reactions": [
                    {"name": reaction.name}
                    for reaction in reactions
                ]
            })

    return {
        "client": {"host": "127.0.0.1"},
        "server": {
            "current_time": int(time.time()),
            "services": services_data
        }
    }
