import uuid
from datetime import datetime

from sqlalchemy import Column, UUID, String, Text, TIMESTAMP, ForeignKey, JSON

from src.database import Base


class News(Base):
    __tablename__ = "news"

    uuid_news = Column(UUID, primary_key=True, default=uuid.uuid4())
    header_news = Column(String, nullable=False, default="HEADER")
    text_news = Column(Text, nullable=True, default="TEXT")
    created_at = Column(TIMESTAMP, default=datetime.utcnow(), nullable=False)
    author_news = Column(String, ForeignKey("user.email_user"), nullable=False)
    images = Column(JSON, default={"paths": []}, nullable=True)
    specific = Column(String, default=None, nullable=True)
