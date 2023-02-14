from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Json


class UserBase(BaseModel):
    email_user: EmailStr


class UserDB(UserBase):
    uuid_user: UUID
    registered_at: datetime
    info_user: Json
    hashed_password_user: str
    role_user: UUID


class User(UserBase):
    registered_at: datetime

    class Config:
        orm_mode = True
