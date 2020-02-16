""" builds nested routes for utils """

from fastapi import APIRouter

from . import ping

def get_router():
    """ returns all routes as nested router in the auth package """

    router = APIRouter()
    router.include_router(ping.router, prefix='/ping', tags=['Health Check'])
    return router
