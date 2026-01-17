from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, database, security
from app.schemas import UserRegister, UserLogin, UserUpdate
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
def register(user_data: UserRegister, db: Session = Depends(database.get_db)):

    existing_email = db.query(models.User).filter(models.User.email == user_data.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already use")

    existing_user = db.query(models.User).filter(models.User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already use")

    hashed = security.hash_password(user_data.password)

    user = models.User(username=user_data.username, email=user_data.email, password=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)

    token_expire = timedelta(minutes= 60 * 24)
    access_token = security.create_access(
        data={"sub": user.email},
        expires_delta=token_expire
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "username": user.username
    }

@router.post("/login")
def login(user_data: UserLogin, db: Session = Depends(database.get_db)):

    user = security.authenticate_user(db, user_data.email, user_data.password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token_expire = timedelta(minutes= 60 * 24)
    access_token = security.create_access(
        data={"sub": user.email},
        expires_delta=token_expire
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "username": user.username
    }

@router.post("/verify")
def verify_token(token: str):
    decode = security.decode_access(token)
    if decode is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )
    return {"valid": True, "email": decode.get("sub")}

@router.get("/me", status_code=status.HTTP_200_OK)
def get_current_user(current_user: models.User = Depends(security.active_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role
    }

@router.get("/me/role")
def get_my_role(current_user: models.User = Depends(security.active_user)):
    return {
        "user_id": current_user.id,
        "role": current_user.role or "user",
        "is_admin": (current_user.role == "admin")
        if current_user.role
            else False
    }

@router.get("/admin/contact-email")
def get_contact_email():
    return {
        "contact": "nanabasave@gmail.com",
    }

@router.get("/users/", dependencies= [Depends(security.require_admin)])
def get_all_users(db: Session = Depends(database.get_db)):
    users = db.query(models.User).all()
    return users

@router.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(security.active_user)):
    if current_user.id != user_id and current_user.role != "admin":
        raise HTTPException(403, "Not authorized")
    
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")
    return user

@router.delete("/users/{user_id}", dependencies=[Depends(security.require_admin)])
def delete_user(user_id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")
    
    db.delete(user)
    db.commit()
    return {"message": f"User {user_id} deleted"}

@router.put("/users/{user_id}")
def update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(database.get_db), current_user: models.User = Depends(security.active_user)):
    if current_user.id != user_id and current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Not authorized to update this user"
        )
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user_data.email and user_data.email != user.email:
        existing_email = db.query(models.User).filter(models.User.email == user_data.email).first()
        if existing_email:
            raise HTTPException(
                status_code=400,
                detail="Email already in use"
            )
        user.email = user_data.email
    
    if user_data.username and user_data.username != user.username:
        existing_username = db.query(models.User).filter(models.User.username == user_data.username).first()
        if existing_username:
            raise HTTPException(
                status_code=400,
                detail="Username already in use"
            )
        user.username = user_data.username
    
    if user_data.password:
        hashed_password = security.hash_password(user_data.password)
        user.password = hashed_password
    
    db.commit()
    db.refresh(user)
    return {
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role
        }
    }

@router.put("/users/{user_id}/role")
def update_user_role(user_id: int, new_role: str, db: Session = Depends(database.get_db)):

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")

    valid_roles = ["user", "admin"]
    if new_role not in valid_roles:
        raise HTTPException(400, f"Role not valid")

    user.role = new_role
    db.commit()
    return {"message": f"User {user_id} role updated to {new_role}"}
