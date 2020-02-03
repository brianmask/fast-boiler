""" Base Model for all API CRUD operations """
# pylint: disable=redefined-builtin

from typing import List, Optional, Generic, TypeVar, Type

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from app.core.db import Base, database

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """ CRUD object with default methods to Create, Read, Update, Delete (CRUD). """

    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model
        self.table = model.__table__

    async def get(self, id: int) -> Optional[ModelType]:
        query = self.table.select().where(id = self.table.c.id)
        return await db_session.query(self.model).filter(self.model.id == id).first()

    async def get_multi(self, db_session: Database, *, skip=0, limit=100) -> List[ModelType]:
        return await db_session.query(self.model).offset(skip).limit(limit).all()

    async def create(self, db_session: Database, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db_session.add(db_obj)
        db_session.commit()
        db_session.refresh(db_obj)
        return db_obj

    def update(
        self, db_session: Database, *, db_obj: ModelType, obj_in: UpdateSchemaType
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(skip_defaults=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db_session.add(db_obj)
        db_session.commit()
        db_session.refresh(db_obj)
        return db_obj

    def remove(self, db_session: Database, *, id: int) -> ModelType:
        obj = db_session.query(self.model).get(id)
        db_session.delete(obj)
        db_session.commit()
        return obj
