""" Application Entrypoint """

from fastapi import FastAPI, Depends
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from app.api.routes import router as api_router
from app.api.security.permissions import get_current_active_user
from app.core import settings
from app.core.db import database
from app.core.middleware import AuthCookieRefresher, RequestResponseTimer

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)


@app.on_event("startup")
async def startup():
    """ Call all startup events """

    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    """ before destroy events """

    await database.disconnect()

# setup CORS through settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS,
    allow_credentials=settings.ALLOW_CREDENTIALS,
    allow_methods=settings.ALLOW_METHODS,
    allow_headers=settings.ALLOW_HEADERS
)

# Add response times to headers
app.add_middleware(RequestResponseTimer)

# Refresh cookie / token on each call
app.add_middleware(AuthCookieRefresher)

# API routes
app.include_router(api_router.get_router(), prefix='/api')

@app.get("/openapi.json", dependencies=[Depends(get_current_active_user)], include_in_schema=False)
async def get_open_api_endpoint():
    """ openapi.json """
    # TODO make this a developer role
    return JSONResponse(get_openapi(title="FastHomeAPI", version=1, routes=app.routes))

@app.get("/docs", dependencies=[Depends(get_current_active_user)], include_in_schema=False)
async def get_documentation():
    """ swagger documentation """
    # TODO make this a developer role
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")

@app.get("/", include_in_schema=False)
async def index():
    """ index """
    return {'msg': 'ok'}
