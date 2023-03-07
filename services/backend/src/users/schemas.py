import uuid
from datetime import datetime

from pydantic import BaseModel, Field, Json, EmailStr, UUID4, StrBytes


class SRoleDB(BaseModel):
    role: str = Field(default="default")
    permissions: Json = Field(default={"permissions": []})

    class Config:
        orm_mode = True


class SUserBase(BaseModel):
    email_user: EmailStr = Field(default=..., title="This is unique user email")


class SUserData(BaseModel):
    fio_user: str = Field(default="professor", title="FIO's professor")
    taught_subject: str = Field(default="subject", title="Subjects taught by a teacher")


class SUserDB(SUserBase):
    uuid_user: UUID4 = Field(default=uuid.uuid4())
    registered_at: datetime = Field(default=datetime.utcnow(), title="This is a datetime registered")
    hashed_password: str = Field(..., title="This is a hashed user password")
    personal_data: SUserData = Field(default=..., title="This is a personal data about user")
    role_user: str = Field(default="default")

    class Config:
        orm_mode = True


class SUser(SUserBase):
    registered_at: datetime = Field(default=datetime.utcnow(), title="This is a datetime registered")
    role_user: str = Field(default="default")


class SUserAD(SUser):
    personal_data: SUserData = Field(default=..., title="This is a personal data about user")
