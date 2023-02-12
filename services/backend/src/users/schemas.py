from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    nickname_user: str
    email_user: EmailStr


class UserDB(UserBase):
    login_user: str
    hashed_password_user: str
    role_user: UUID


class User(UserDB):
    uuid_user: UUID
    registered_at: datetime

    class Config:
        orm_mode = True
