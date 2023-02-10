from uuid import UUID
from datetime import datetime
from pathlib import Path

from pydantic import BaseModel, Field


class Image(BaseModel):
    path_to_image: Path


class Post(BaseModel):
    id: UUID = Field(default="UUID")
    date: datetime = Field(default=datetime.utcnow(), title="Time creation current post")
    author: UUID = Field(default="UUID", title="The UUID author post")
    header: str = Field(default="", title="The header current post")
    text: str = Field(default="", title="The text current post")
    images: list[Image]
