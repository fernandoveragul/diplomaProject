import uuid
from datetime import datetime

from pydantic import BaseModel, Field, EmailStr, UUID4


class SRole(BaseModel):
    role: str = Field(default="default")


class SRoleDB(SRole):
    permissions: list[str] = Field(default=[""])

    class Config:
        orm_mode = True


class SUserBase(BaseModel):
    email_user: EmailStr = Field(default=..., title="This is unique user email", alias="emailUser")


class SUserData(BaseModel):
    fio_user: str = Field(default="professor", title="FIO's professor", alias="fioUser")
    taught_subject: str = Field(default="subject", title="Subjects taught by a teacher", alias="taughtSubject")


class SUserDB(SUserBase):
    uuid_user: UUID4 = Field(default=uuid.uuid4(), alias="uuidUser")
    registered_at: datetime = Field(default=datetime.utcnow(), title="This is a datetime registered",
                                    alias="registeredAt")
    hashed_password: str = Field(..., title="This is a hashed user password", alias="hashedPassword")
    personal_data: SUserData = Field(default=..., title="This is a personal data about user", alias="personalData")
    role_user: str = Field(default="default", alias="roleUser")

    class Config:
        orm_mode = True


class SUser(SUserBase):
    role_user: str = Field(default="default", alias="roleUser")


class SUserAD(SUser):
    personal_data: SUserData = Field(default=..., title="This is a personal data about user", alias="personalData")
