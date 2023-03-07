import uuid
from datetime import datetime

from sqlalchemy import Column, UUID, String, TIMESTAMP, ForeignKey, JSON

from src.database import Base


class MRoleUser(Base):
    __tablename__ = "role"
    role = Column(String, primary_key=True, default="default")
    permissions = Column(JSON, nullable=False)


class MUser(Base):
    __tablename__ = "user"

    uuid_user = Column(UUID, primary_key=True, default=uuid.uuid4())
    registered_at = Column(TIMESTAMP, default=datetime.utcnow(), nullable=False)
    email_user = Column(String, index=True, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    personal_data = Column(JSON, nullable=False)
    role_user = Column(String, ForeignKey('role.role'), nullable=False, default="default")
