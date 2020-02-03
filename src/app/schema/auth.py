""" Schema for Auth Models """

from typing import List, Optional

from pydantic import BaseModel


class GroupBase(BaseModel):
    """ Base Schema for Groups """
    name: str


class GroupBaseDB(GroupBase):
    """ Base Schema for DB """
    id: int


class Group(GroupBaseDB):
    """ Final Schema for API """


class UserBase(BaseModel):
    """ Base Schema for User to allow fine tuning of API """
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False


class UserBaseDB(UserBase):
    """ Base Schema for User after DB save """
    id: int = None

    class Config:
        """ orm mode """
        orm_mode = True


class UserCreate(UserBaseDB):
    """ Add required fields required to create a user """
    username: str
    password: str


class UserUpdate(UserBaseDB):
    """ Schema to allow user to update password """
    password: Optional[str] = None


class User(UserBaseDB):
    """ Many to many fields returned by API """
    groups: Optional[List] = None


class UserDB(UserBaseDB):
    """ Final DB Object """
    hashed_password: str
