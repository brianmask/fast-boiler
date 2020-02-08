""" basic healthcheck """

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def pong():
    """basic healthcheck

    Request Type: GET
    endpoint /ping

    :returns JSONResponse {"ping": "pong!"}
    """

    return {"ping": "pong!"}
