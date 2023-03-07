import uuid
from datetime import datetime

from pydantic import Field, EmailStr, UUID4, BaseModel


class SImages(BaseModel):
    paths: list[str] = Field(default=[], title="This is a list paths to images current news post")


class SNewsPostData(BaseModel):
    uuid_news: UUID4 = Field(default=uuid.uuid4())
    author_news: EmailStr = Field(default=..., title="This is an author news post")


class SNews(BaseModel):
    header_news: str = Field(default="HEADER", title="This is a header news post")
    text_news: str = Field(default="TEXT", title="This is a text news post")
    author_news: EmailStr = Field(default=..., title="This is an author news post")
    images: SImages = Field(default=..., title="This is a list paths to images current news post")


class SNewsDB(SNews):
    uuid_news: UUID4 = Field(default=uuid.uuid4())
    created_at: datetime = Field(default=datetime.utcnow())
    specific: str | None = Field(default=None, title="This is a specific type news post")

    class Config:
        orm_mode = True


class SNewsAD(SNews):
    specific: str | None = Field(default=None, title="This is a specific type news post")
