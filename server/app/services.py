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
