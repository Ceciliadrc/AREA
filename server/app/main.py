from fastapi import FastAPI, Depends
import time
from app import models, database
from sqlalchemy.orm import Session
from auth import router as auth_router
from areas import router as areas_router
from services import router as services_router

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

    services_list = []
    services = db.query(models.Service).all()

    # for service in services:
    #     actions =

    return {
        "client": {"host": "127.0.0.1"},
        "server": {
            "current_time": int(time.time()),
            "services": services_list
        }
    }
# main a finir