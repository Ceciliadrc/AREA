from app import models, database, security
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .actionConfig import ACTION_CONFIGS, REACTION_CONFIGS
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
            "description": action.description
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
            "description": reaction.description
        }
        for reaction in reactions
        ]
    }

@router.get("/actions/{service_name}/{action_name}")
def get_action_config(service_name: str, action_name: str):
    config = ACTION_CONFIGS.get(service_name, {}).get(action_name, {})
    return {
        "service": service_name,
        "action": action_name,
        **config
    }

@router.get("/reactions/{service_name}/{reaction_name}")
def get_reaction_config(service_name: str, reaction_name: str):
    config = REACTION_CONFIGS.get(service_name, {}).get(reaction_name, {})
    return {
        "service": service_name,
        "reaction": reaction_name,
        **config
    }

@router.get("/users/{user_id}/credentials")
def get_user_credentials(user_id: int,db: Session = Depends(database.get_db),current_user: models.User = Depends(security.active_user)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # recupere services connecte
    user_tokens = db.query(models.UserOauth).filter(models.UserOauth.user_id == user_id).all()
    
    credentials = []
    for token in user_tokens:
        service = db.query(models.Service).filter(
            models.Service.id == token.service_id
        ).first()
        
        if service:
            credentials.append({
                "service_id": service.id,
                "service_name": service.name,
                "display_name": service.display_name,
                "connected": True,
                "has_token": bool(token.access_token),
                "provider_user_id": token.provider_user_id
            })
    return {
        "user_id": user_id,
        "username": user.username,
        "email": user.email,
        "connected_services": credentials,
        "total_connected": len(credentials)
    }