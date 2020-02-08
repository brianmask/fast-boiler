""" Base Model for all API CRUD operations """
# pylint: disable=redefined-builtin

from typing import List, Optional, Generic, TypeVar, Type

from pydantic import BaseModel
from sqlalchemy import Table

from app.core.db import  database

TableType = TypeVar("TableType", bound=Table)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[TableType, CreateSchemaType, UpdateSchemaType]):
    """ CRUD object with default methods to Create, Read, Update, Delete (CRUD). """

    def __init__(self, table: Type[TableType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `table`: A SQLAlchemy table
        * `schema`: A Pydantic model (schema) class
        """
        self.table = table

    async def get(self, id: int) -> Optional[TableType]:
        """ implements get /id/ """

        query = self.table.select().where(id == self.table.c.id)
        return await database.fetch_one(query=query)

    async def get_multi(self, *, skip=0, limit=100) -> List[TableType]:
        """ implements get /?skip=0&limit=100 if limit=0 all results are returned
        regardless of skip
        """

        query = self.table.select()
        if limit > 0:
            query = query.offset(skip).limit(limit)
        return await database.fetch_all(query=query)

    async def create(self, *, obj_in: CreateSchemaType) -> TableType:
        """ implements post / """

        query = self.table.insert().values(**obj_in.dict())
        return await database.execute(query=query)

    async def update(self, *, db_obj: TableType, obj_in: UpdateSchemaType) -> TableType:
        """ implements put /id/ """

        query = (
            self.table
            .udate()
            .where(db_obj.id == self.table.id)
            .values(**obj_in.dict(skip_defaults=True))
            .returning(self.table.c.id)
        )
        return await database.execute(query=query)

    async def remove(self, *, id: int) -> TableType:
        """ impplements delete /id/ """

        query = self.table.delete().where(id == self.table.c.id)
        return await database.execute(query=query)
