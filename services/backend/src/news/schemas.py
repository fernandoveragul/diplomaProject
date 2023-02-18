import uuid
from uuid import UUID
from datetime import datetime
from pathlib import Path

from pydantic import BaseModel, Field


class Image(BaseModel):
    paths_to_image: list[str] = Field(default=..., include=False)


class Post(BaseModel):
    uuid_post: UUID = Field(default=uuid.uuid4())
    time_post: datetime = Field(default=datetime.utcnow(), title="Time creation current post")
    author_post: UUID = Field(default=uuid.uuid4(), title="The UUID author post")
    header_post: str = Field(default="", title="The header current post")
    text_post: str = Field(default="", title="The text current post")
    images: Image | None = Field(default=..., include=False)

    class Config:
        orm_mode = True
