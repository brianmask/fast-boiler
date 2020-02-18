""" User specific CRUD Class """

import re
from typing import Optional

from asyncpg import exceptions

from app.core.db import database
from app.core.exceptions import CRUDError
from app.core.security.password import verify_password, get_password_hash
from app.crud.base import CRUDBase
from app.helpers.expressions import VALID_EMAIL
from app.models.auth import user
from app.schema.auth import UserCreate, UserUpdate, UserDBCreate, User, UserDB


class UserCRUD(CRUDBase[User, UserCreate, UserUpdate]):
    """ CRUD Actions for USER table """

    def __init__(self, table=user):
        """ initialize the handler """

        super().__init__(table)

    async def get_by_email_or_username(self, *, identification: str) -> Optional[UserDB]:
        """ retrieves a user object by either email or username """

        if re.search(VALID_EMAIL, identification):
            query = self.table.select().where(identification == user.c.email)
        else:
            query = self.table.select().where(identification == user.c.username)

        return await database.fetch_one(query=query)

    async def create(self, *, obj_in: UserCreate) -> user:
        """ create a new user object """

        obj_out = UserDBCreate(**obj_in.dict())
        obj_out.hashed_password = get_password_hash(obj_in.password)
        query = self.table.insert().values(**obj_out.dict())
        try:
            user_id = await database.execute(query=query)
        except (exceptions.PostgresError, exceptions.PostgresWarning) as exc:
            raise CRUDError(exc)

        return await self.get(user_id)

    async def authenticate(self, *, identification: str, password: str) -> Optional[User]:
        """ authenticate the user - return user or none """

        record = await self.get_by_email_or_username(identification=identification)

        if not record:
            return None

        if not verify_password(password, record['hashed_password']):
            return None

        return record

    def is_active(self, user_obj: User) -> bool:
        """ returns true if user is currently active """

        return user_obj['is_active']

    def is_superuser(self, user_obj: User) -> bool:
        """ returns true if user is superuser """

        return user_obj['is_superuser']

USER_CRUD = UserCRUD()
