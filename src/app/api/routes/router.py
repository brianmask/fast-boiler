""" builds nested routes for api """

from fastapi import APIRouter

from . import ping
from .auth import router as auth_router

def get_router():
    """ returns all routes as nested router in the api package """

    router = APIRouter()
    router.include_router(ping.router, prefix='/ping', tags=['Healthcheck'])
    router.include_router(auth_router.get_router(), prefix='/auth', tags=['Auth Actions'])

    return router
