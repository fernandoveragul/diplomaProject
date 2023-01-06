from sqlalchemy import MetaData, Table, Column
from sqlalchemy import Integer, JSON

metadata = MetaData()

role = Table(
    "role",
    metadata,
    Column("id_role", Integer, primary_key=True),
    Column("name", nullable=False),
    Column("permissions", JSON)
)
