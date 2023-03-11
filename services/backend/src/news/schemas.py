import uuid
from datetime import datetime

from pydantic import Field, EmailStr, UUID4, BaseModel


class SImages(BaseModel):
    paths: list[str] = Field(default=[""], title="This is a list paths to images current news post")


class SNewsPostBase(BaseModel):
    author_news: EmailStr = Field(default=..., title="This is an author news post", alias="authorNews")


class SNews(SNewsPostBase):
    header_news: str = Field(default="HEADER", title="This is a header news post", alias="headerNews")
    text_news: str = Field(default="TEXT", title="This is a text news post", alias="textNews")
    images: SImages | None = Field(default=None, title="This is a list paths to images current news post")
    specific: str | None = Field(default=None, title="This is a specific type news post")


class SNewsAD(SNews):
    uuid_news: UUID4 = Field(default=uuid.uuid4(), alias="uuidNews")
    created_at: datetime = Field(default=datetime.utcnow(), alias="createdAt")


class SNewsDB(SNewsAD):

    class Config:
        orm_mode = True
