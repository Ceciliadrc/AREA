from app import models, database
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(prefix="/areas", tags=["areas"])

@router.post("/")
def create_area(name: str, user_id: int, action_id: int, reaction_id: int, db: Session = Depends(database.get_db)):

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")
    
    new_area = models.Area(
        name=name,
        user_id=user_id,
        action_id=action_id,
        reaction_id=reaction_id
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