""" builds nested routes for auth """

from fastapi import APIRouter

from . import user

def get_router():
    """ returns all routes as nested router in the auth package """

    router = APIRouter()
    router.include_router(user.router, prefix='/users', tags=['User Actions'])

    return router
