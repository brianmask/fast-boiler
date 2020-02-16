""" basic healthcheck """

from fastapi import APIRouter, Depends

from app.api.security.permissions import get_token_payload

router = APIRouter()


@router.get("/ping", dependencies=[Depends(get_token_payload)])
async def pong():
    """basic healthcheck

    Request Type: GET
    endpoint /ping

    :returns JSONResponse {"ping": "pong!"}
    """

    return {"ping": "pong!"}
