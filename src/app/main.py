""" Application Entrypoint """

import time

from fastapi import FastAPI, Depends
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.api.routes import router as api_router
from app.api.security.permissions import get_current_active_user
from app.core.db import database

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
#app = FastAPI()


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

@app.get("/openapi.json", dependencies=[Depends(get_current_active_user)], include_in_schema=False)
async def get_open_api_endpoint():
    """ openapi.json """
    # TODO make this a developer role
    return JSONResponse(get_openapi(title="fast_home - API", version=1, routes=app.routes))

@app.get("/docs", dependencies=[Depends(get_current_active_user)], include_in_schema=False)
async def get_documentation():
    """ swagger documentation """
    # TODO make this a developer role
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")

@app.get("/", include_in_schema=False)
async def index():
    """ index """
    return {'msg': 'ok'}
