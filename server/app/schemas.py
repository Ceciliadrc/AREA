from pydantic import BaseModel, EmailStr
from typing import Optional, List

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    
    class Config:
        from_attributes = True

class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    
    class Config:
        from_attributes = True

class AreaBase(BaseModel):
    name: str
    user_id: int
    action_id: int
    reaction_id: int

class AreaResponse(UserBase):
    id: int
    name: str
    user_id: int
    action_id: int
    reaction_id: int
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    username: str

class TokenData(BaseModel):
    email: Optional[str] = None

class ServiceBase(BaseModel):
    name: str
    display_name: str

class ServiceResponse(ServiceBase):
    id: int
    action: List[str] = []
    reaction: List[str] = []

    class Config:
        from_attributes = True