from typing import Optional
from pydantic import BaseModel, EmailStr
import datetime

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    full_name: Optional[str] = None
    role: Optional[str] = "USER" # Validated server-side

class UserLogin(BaseModel):
    email: str # email or username
    password: str
    role: Optional[str] = None # Informational only; role is enforced by backend account

class UserResponse(BaseModel):
    id: int
    uuid: str
    email: str
    username: str
    full_name: Optional[str] = None
    role: str
    is_active: bool
    created_at: datetime.datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class TokenData(BaseModel):
    user_id: Optional[int] = None
    email: Optional[str] = None
    role: Optional[str] = None
