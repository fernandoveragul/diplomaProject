import uuid
from datetime import datetime

from pydantic import Field, EmailStr, UUID4, BaseModel, Json


class News(BaseModel):
    header_news: str = Field(default="HEADER", title="This is a header news post")
    text_news: str = Field(default="TEXT", title="This is a text news post")
    created_at: datetime = Field(default=datetime.utcnow())
    author_news: EmailStr = Field(default="user@usr.com", title="This is an author news post")
    images: Json = Field(default={"paths": []}, title="This is a list paths to images current news post")


class NewsDB(News):
    uuid_news: UUID4 = Field(default=uuid.uuid4())
    specific: str | None = Field(default=None, title="This is a specific type news post")

    class Config:
        orm_mode = True


class NewsAD(News):
    specific: str | None = Field(default=None, title="This is a specific type news post")
