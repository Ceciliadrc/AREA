from app import models, database
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(prefix="/services", tags=["services"])

@router.get("/")
def get_all_services(db: Session = Depends(database.get_db)):

    services = db.query(models.Service).all()

    return {
        "services": [
            {
                "id": service.id,
                "name": service.name,
                "display_name": service.display_name
            }
            for service in services
        ]
    }

@router.get("/{service_id}")
def get_one_service(service_id: int, db: Session = Depends(database.get_db)):

    service = db.query(models.Service).filter(models.Service.id == service_id).first()

    if not service:
        raise HTTPException(404, "Service not found")
    
    return {
        "id": service.id,
        "name": service.name,
        "display_name": service.display_name
    }

@router.get("/{service_id}/actions")
def get_service_action(service_id: int, db: Session = Depends(database.get_db)):

    actions = db.query(models.Action).filter(models.Action.service_id == service_id).all()

    return {
        "service_id": service_id,
        "actions": [{
            "id": action.id,
            "name": action.name,
        }
        for action in actions
        ]
    }

@router.get("/{service_id}/reactions")
def get_service_reaction(service_id: int, db: Session = Depends(database.get_db)):

    reactions = db.query(models.Reaction).filter(models.Reaction.service_id == service_id).all()

    return {
        "service_id": service_id,
        "reactions": [{
            "id": reaction.id,
            "name": reaction.name,
        }
        for reaction in reactions
        ]
    }
