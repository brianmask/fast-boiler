""" logout route, clear cookie, blacklist token """

from fastapi import APIRouter
from starlette.responses import RedirectResponse

router = APIRouter()

@router.get("")
async def route_logout_and_remove_cookie():
    """ Logout and remove cookie #TODO blacklist token, remove session """

    response = RedirectResponse(url="/")
    response.delete_cookie("Authorization")
    return response
