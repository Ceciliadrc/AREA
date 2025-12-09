from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    
    class Config:
        from_attributes = True

class AreaBase(BaseModel):
    name: str
    user_id: int
    action_id: int
    reaction_id: int

class AreaResponse(UserBase):
    id: int
    
    class Config:
        from_attributes = True
