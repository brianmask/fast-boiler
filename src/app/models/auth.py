""" All Auth based Tables (Users, Groups) """

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import relationship

from app.core.db import Base

user_groups = Table(
    'user_groups',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('group_id', Integer, ForeignKey('group.id')),
)

class Group(Base):
    """ Base Group Class - Roles """

    # Group ID
    id = Column(Integer, primary_key=True, index=True)

    # Group Name
    name = Column(String(length=45), unique=True, index=True)


class User(Base):
    """ Base User Class """

    # ID of the user
    id = Column(Integer, primary_key=True, index=True)

    # Username
    username = Column(String(length=20), unique=True, index=True)

    # Firstname
    first_name = Column(String(length=25), nullable=True)

    # Lastname
    last_name = Column(String(length=40), nullable=True)

    # User email address
    email = Column(String(length=155), unique=True, nullable=True, index=True)

    # User Password
    hashed_password = Column(Text)

    # Is the user currently active?
    is_active = Column(Boolean(), default=True)

    # Grant all permissions?
    is_superuser = Column(Boolean(), default=False)

    # User Groups
    groups = relationship('Group', secondary=USER_GROUPS, backref='users')
