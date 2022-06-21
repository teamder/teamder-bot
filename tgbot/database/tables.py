"""Contains database tables info"""
from datetime import datetime

from sqlalchemy import MetaData, Table, Column
from sqlalchemy import BigInteger, Integer, DateTime
from sqlalchemy import String, Text

metadata = MetaData()

users = Table(
    "users", metadata,
    Column("user_id", BigInteger(), primary_key=True),
    Column("firstname", String(), nullable=False),
    Column("lastname", String(), nullable=True),
    Column("fullname", String(), nullable=False),
    Column("username", String(), nullable=True),
    Column("lang", String(), default="ru"),
    Column("created_on", DateTime(), default=datetime.now),
    Column(
        "updated_on", DateTime(),
        default=datetime.now, onupdate=datetime.now
    )
)


admins = Table(
    "admins", metadata,
    Column("user_id", BigInteger(), primary_key=True),
    Column("created_on", DateTime(), default=datetime.now),
    Column(
        "updated_on", DateTime(),
        default=datetime.now, onupdate=datetime.now
    )
)

projects = Table(
    "projects", metadata,
    Column("project_id", Integer(), primary_key=True),
    Column("owner_id", BigInteger(), nullable=False),
    Column("name", String()),
    Column("description", Text()),
    Column("members", Text()),
    Column("created_on", DateTime(), default=datetime.now),
)
