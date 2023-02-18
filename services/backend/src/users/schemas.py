import uuid
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Json, Field


class UserBase(BaseModel):
    email_user: EmailStr = Field(default="gapouso@amt.com", title="EMail user")


class UserDB(UserBase):
    uuid_user: UUID = Field(default=uuid.uuid4(), title="UUID user")
    registered_at: datetime = Field(default=datetime.utcnow(), title="DateTime registered user")
    info_user: Json = Field(..., title="Confid info")
    hashed_password_user: str = Field(...)
    role_user: UUID = Field(...)


class User(UserBase):
    registered_at: datetime = Field(default=datetime.utcnow(), title="DateTime registered user")

    class Config:
        orm_mode = True
