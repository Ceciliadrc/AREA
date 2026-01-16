##
## EPITECH PROJECT, 2025
## AREA
## File description:
## authOpenAi
##

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import os
from app import models, database

router = APIRouter(prefix="/auth", tags=["auth"])

class OpenAiConfig:
    api_key = os.getenv("OPENAI_API_KEY")

@router.post("/openai/connect")
def connectOpenAi(user_id: int, db: Session = Depends(database.get_db)):
    """Connecte un utilisateur à OpenAI avec sa clé API"""
    
    if not OpenAiConfig.api_key:
        raise HTTPException(500, "OpenAI API key not configured in .env")
    
    service = db.query(models.Service).filter(models.Service.name == "openai").first()
    
    if not service:
        raise HTTPException(500, "OpenAI service not found in database")
    
    from app.oauthDbConfig import OauthDbConfig
    OauthDbConfig.save_user(
        db=db,
        user_id=user_id,
        service_id=service.id,
        access_token=OpenAiConfig.api_key
    )
    
    return {
        "message": "OpenAI connected successfully!",
        "service": "openai",
        "key_length": len(OpenAiConfig.api_key),
        "key_preview": f"{OpenAiConfig.api_key[:10]}...{OpenAiConfig.api_key[-4:]}"
    }

# Route GET pour compatibilité (optionnelle)
@router.get("/openai/login")
def logWithOpenai(user_id: int):
    """Endpoint GET qui redirige vers la méthode POST"""
    raise HTTPException(
        405, 
        detail="Use POST /auth/openai/connect instead. Example: curl -X POST 'http://localhost:8080/auth/openai/connect?user_id=1'"
    )

# Route de test
@router.get("/openai/check")
def checkOpenAiConfig():
    """Vérifie la configuration OpenAI"""
    key = OpenAiConfig.api_key
    return {
        "configured": bool(key),
        "key_length": len(key) if key else 0,
        "key_preview": f"{key[:10]}...{key[-4:]}" if key and len(key) > 14 else "N/A",
        "status": "OK" if key else "ERROR"
    }