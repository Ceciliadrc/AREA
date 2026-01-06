from pydantic import BaseModel, EmailStr

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
