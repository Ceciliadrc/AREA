from fastapi import FastAPI, Depends
import time
from app import models, database
from sqlalchemy.orm import Session
from .auth import router as auth_router
from .areas import router as areas_router
from .services import router as services_router
from sqlalchemy import exc

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
