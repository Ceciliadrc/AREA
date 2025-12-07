from fastapi import FastAPI, Depends
import time
from app import models, database
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "API is working"}

@app.get("/about.json")
async def about():
    return {
        "client": {"host": "127.0.0.1"},
        "server": {
            "current_time": int(time.time()),
            "services": []
        }
    }
