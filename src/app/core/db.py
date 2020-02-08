""" initialize the database """
# pylint: disable=invalid-name

from databases import Database
from sqlalchemy import MetaData

from . import settings


DATABASE_URL = settings.DATABASE_URL

metadata = MetaData()

# databases query builder
database = Database(DATABASE_URL)
