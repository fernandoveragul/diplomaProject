import uuid
from datetime import datetime

from sqlalchemy import MetaData
from sqlalchemy import Table, Column, JSON, String, TIMESTAMP, UUID, ForeignKey

users_meta = MetaData()


role: Table = Table(
    "role",
    users_meta,
    Column("uuid_role", UUID, index=True, primary_key=True, default=uuid.uuid4),
    Column("role_name", String, nullable=False),
    Column("preferences_user", JSON, nullable=False)
)

user: Table = Table(
    "user",
    users_meta,
    Column("uuid_user", UUID, index=True, primary_key=True, default=uuid.uuid4),
    Column("registered_at", TIMESTAMP, nullable=False, default=datetime.utcnow),
    Column("email_user", String, nullable=False, unique=True),
    Column("hashed_password_user", String, nullable=False),
    Column("info_user", JSON, nullable=False),
    Column("role_user", UUID, ForeignKey(role.c.uuid_role))
)
