from fastapi import FastAPI, Depends
import time
from app import models, database
from sqlalchemy.orm import Session
from app.auth import router as auth_router
from app.areas import router as areas_router
from app.services import router as services_router

models.Base.metadata.create_all(bind=database.engine) # cree les tables

app = FastAPI()

app.include_router(auth_router)
app.include_router(areas_router)
app.include_router(services_router)

@app.get("/")
async def root():
    return {"message": "API is working"}

@app.get("/about.json")
async def about(db: Session = Depends(database.get_db)):

    services_data = []
    services = db.query(models.Service).all()

    for service in services:
        actions = db.query(models.Action).filter(models.Action.service_id == service.id).all()
    
    for service in services:
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
