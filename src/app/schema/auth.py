""" Schema for Auth Models """
# pylint: disable=no-self-argument

import re
from typing import Dict, List, Optional

from pydantic import BaseModel, validator

from app.core.security.password import validate_password
from app.helpers.expressions import VALID_EMAIL


class GroupBase(BaseModel):
    """ Base Schema for Groups """
    name: str
    description: Optional[str] = None

class GroupBaseDB(GroupBase):
    """ Base Schema for DB """
    id: int


class Group(GroupBaseDB):
    """ Final Schema for API """


class UserBasic(BaseModel):
    """ Basic user info - combine with id to give clients linking and list abilities """

    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserBase(UserBasic):
    """ Base Schema for User with optional data to be collected"""

    username: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False

    @validator('email')
    def validate_email(cls, value):
        """ validates the email provided is valid form """

        if value is not None and not re.search(VALID_EMAIL, value):
            raise ValueError('email address is not valid')

        return value

    @validator('username')
    def validate_username(cls, value):
        """ validates the username is alphanumeric """

        if value is not None and not value.isalnum():
            raise ValueError('username must be alphanumeric')

        return value


class UserBaseDB(UserBase):
    """ Base Schema for User after DB save to return most non sensitive data """

    id: int = None


class UserList(UserBasic):
    """ Add ID into UserBasic so we can provide a list for linking and name building """

    id: int

def password(value: str, values: Dict[str, str]) -> str:
    """ make sure the password supplied meets our criteria """

    # We will assume all attempts will fail so start with least intense first
    if 'password' not in values or value != values['password']:
        raise ValueError('passwords do not match')

    # Validate returns True if valid, or raises Value error if not
    validate_password(value)

    return value

class UserCreate(UserBase):
    """ Add required fields required to create a user """

    password: str
    password_validate: str

    _validate_password = validator('password_validate', allow_reuse=True, always=True)(password)


class UserUpdate(UserBaseDB):
    """ Schema to allow user to update password """

    password: Optional[str] = None


class User(UserBaseDB):
    """ Does not include hashed password, could include other extra's """

    groups: Optional[List] = None

class UserDB(UserBaseDB):
    """ Final DB Object """

    hashed_password: str

class UserDBCreate(UserBase):
    """ Object to save in the database / does not include key """

    hashed_password: Optional[str] = None
