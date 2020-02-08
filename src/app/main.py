""" Application Entrypoint """

import time

from fastapi import FastAPI
from starlette.requests import Request

from app.api.routes import router as api_router
from app.core.db import database

app = FastAPI()


@app.on_event("startup")
async def startup():
    """ Call all startup events """

    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    """ before destroy events """

    await database.disconnect()

@app.middleware('http')
async def add_process_time_header(request: Request, call_next):
    """ add system time spent on api call to header """

    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers['X-Process-Time'] = str(process_time)
    return response

app.include_router(api_router.get_router(), prefix='/api')
