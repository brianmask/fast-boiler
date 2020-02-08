""" All Auth based Tables (Users, Groups) """

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
)
from sqlalchemy.sql import func

from app.core.db import metadata

# Many to Many: User -> Groups
# Permissions / Roles
user_groups = Table(
    'user_groups',
    metadata,
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('group_id', Integer, ForeignKey('group.id')),
)

# Permission / Role Groups
group = Table(
    'group',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(length=45), unique=True, index=True, nullable=False),
    Column('description', Text)
)

# Base User Data
user = Table(
    'user',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('username', String(length=20), unique=True, index=True),
    Column('first_name', String(length=25)),
    Column('last_name', String(length=40)),
    Column('email', String(length=155), unique=True, index=True),
    Column('hashed_password', Text, nullable=False),
    Column('is_active', Boolean(), default=True, nullable=False),
    Column('is_superuser', Boolean(), default=False, nullable=False),
    Column('date_joined', DateTime, default=func.now(), nullable=False),
    Column('last_login', DateTime),
)
