""" builds nested routes for api """

from fastapi import APIRouter

from .auth import router as auth_router
from .utils import router as utils_router

def get_router():
    """ returns all routes as nested router in the api package """

    router = APIRouter()
    router.include_router(utils_router.get_router(), prefix='/utils', tags=['Utilities'])
    router.include_router(auth_router.get_router(), prefix='/auth', tags=['Auth Actions'])

    return router
