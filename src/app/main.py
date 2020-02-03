""" Application Entrypoint """

from fastapi import FastAPI

from app.api.routes import ping
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

app.include_router(ping.router)
