from sqlalchemy import MetaData, Table, Column
from sqlalchemy import Integer, String, JSON

metadata: MetaData = MetaData()

role: Table = Table(
    "role",
    metadata,
    Column("id_role", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("permissions", JSON)
)
