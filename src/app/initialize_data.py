""" create initial datasets """
import asyncio
import logging

from app import crud
from app.core import settings
from app.core.db import database
from app.schema.auth import UserCreate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def init_db():
    """ Initialize the database with data """

    # Does the superuser already exist?
    user = await crud.user.get_by_email_or_username(identification=settings.FIRST_USER)
    if not user:
        # Create it
        user_in = UserCreate(
            username=settings.FIRST_USER,
            password=settings.FIRST_PASSWORD,
            password_validate=settings.FIRST_PASSWORD,
            is_superuser=True,
        )
        await crud.user.create(obj_in=user_in)

async def init():
    """ do connect, do data, do disconnect """

    await database.connect()
    await init_db()
    await database.disconnect()

if __name__ == '__main__':
    asyncio.run(init())
