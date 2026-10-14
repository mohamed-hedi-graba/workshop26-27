from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class RegisterIn(BaseModel):
    username: str
    email: EmailStr
    password: str


class LoginIn(BaseModel):
    username: str
    password: str


class UserPublic(BaseModel):
    id: str
    username: str
    email: str

    class Config:
        from_attributes = True


class UserFull(BaseModel):
    id: str
    username: str
    email: str
    password: str
    role: str
    bio: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class PostOut(BaseModel):
    id: int
    author_id: str
    title: str
    content: str
    image_path: Optional[str] = None
    visibility: str
    created_at: datetime

    class Config:
        from_attributes = True
