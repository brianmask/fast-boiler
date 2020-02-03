from fastapi import APIRouter

router = APIRouter()


@router.get("/ping")
async def pong():
    """basic healthcheck
    
    Request Type: GET
    endpoint /ping

    :returns JSONResponse {"ping": "pong!"}   
    """
    
    return {"ping": "pong!"}
