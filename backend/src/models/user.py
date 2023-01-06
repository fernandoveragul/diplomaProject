from datetime import datetime

from sqlalchemy import MetaData, Table, Column, ForeignKey
from sqlalchemy import Integer, String, TIMESTAMP

from .role import role

metadata = MetaData()

user = Table(
    "user",
    metadata,
    Column("id_user", Integer, primary_key=True),
    Column("email", String, nullable=False),
    Column("nickname", String, nullable=False),
    Column("hashed_password", String, nullable=False),
    Column("registered_at", TIMESTAMP, default=datetime.utcnow),
    Column("role_id", Integer, ForeignKey(role.c.id)),
)
