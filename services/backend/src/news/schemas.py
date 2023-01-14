from datetime import datetime
from pydantic import BaseModel


class Post(BaseModel):
    id: int
    date: datetime
    author: str
    text: str
    images: list[str]
