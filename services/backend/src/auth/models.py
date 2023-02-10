import datetime

from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, UUID

auth_meta = MetaData()

user = Table(
    "users",
    auth_meta,
    Column("id", UUID, primary_key=True),
    Column("name", String, nullable=False),
    Column("registered_at", TIMESTAMP, nullable=False, default=datetime.datetime.utcnow)
)
