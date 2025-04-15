from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    username: EmailStr
    password: str

class UserCreate(UserBase):
    pass

class UserLogin(UserBase):
    pass

class Token(BaseModel):
    message: str
    auth_key: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None