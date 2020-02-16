""" builds nested routes for auth """

from fastapi import APIRouter

from . import user, login, logout

def get_router():
    """ returns all routes as nested router in the auth package """

    router = APIRouter()
    router.include_router(user.router, prefix='/users', tags=['User Actions'])
    router.include_router(login.router, prefix='/login', tags=['Login Actions'])
    router.include_router(logout.router, prefix='/logout', tags=['Login Actions'])
    return router
