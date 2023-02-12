import uuid
from datetime import datetime

from sqlalchemy import MetaData, Table, Column, JSON
from sqlalchemy import UUID, TIMESTAMP, String

news_meta = MetaData()

posts: Table = Table(
    "posts",
    news_meta,
    Column("uuid_post", UUID, primary_key=True, index=True, default=uuid.uuid4),
    Column("time_post", TIMESTAMP, nullable=False, default=datetime.utcnow),
    Column("author_post", UUID, nullable=False),
    Column("header_post", String, nullable=False),
    Column("text_post", String),
    Column("images_post", JSON, nullable=True)
)
