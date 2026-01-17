from app import models, database
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

router = APIRouter(prefix="/areas", tags=["areas"])

@router.post("/")
def create_area(name: str, user_id: int, action_service: str, action_name: str, reaction_service: str, reaction_name: str, db: Session = Depends(database.get_db), parameters: Optional[str] = Query(None)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")
    
    action = db.query(models.Action).join(models.Service).filter(
        models.Service.name == action_service,
        models.Action.name == action_name).first()
    
    if not action:
        raise HTTPException(404, f"Action {action_service}.{action_name} not found")
    
    reaction = db.query(models.Reaction).join(models.Service).filter(
        models.Service.name == reaction_service,
        models.Reaction.name == reaction_name).first()
    
    if not reaction:
        raise HTTPException(404, f"Reaction {reaction_service}.{reaction_name} not found")
    
    new_area = models.Area(
        name=name,
        user_id=user_id,
        action_id=action.id,
        reaction_id=reaction.id,
        parameters=parameters
    )
    db.add(new_area)
    db.commit()
    db.refresh(new_area)

    return {
        "message": "AREA created",
        "name": new_area.name 
    }

@router.get("/")
def get_user_areas(user_id: int, db: Session = Depends(database.get_db)):

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")

    areas = db.query(models.Area).filter(models.Area.user_id == user_id).all()

    return {
        "user_id": user_id,
        "username": user.username,
        "areas": [
            {
                "id": area.id,
                "name": area.name,
                "action_id": area.action_id,
                "reaction_id": area.reaction_id
            }
            for area in areas
        ]
    }

@router.delete("/{area_id}")
def delete_area(area_id: int, db: Session = Depends(database.get_db)):

    area = db.query(models.Area).filter(models.Area.id == area_id).first()

    if not area:
        raise HTTPException(404, "Area not found")
    
    db.delete(area)
    db.commit()

    return {
        "message": "Area delete"
    }
