""" endpoints to hande basic authentication """

import base64

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm

from starlette.responses import JSONResponse, RedirectResponse, Response

from app import crud
from app.core.security.token import create_access_token_jwt, add_response_auth_cookie
from app.core.security.backends import BasicAuth, basic_auth
from app.schema.token import Token

router = APIRouter()

async def _validate_user(*, username: str, password: str) -> Token:
    """ check if user credentials are valid

    :param username: username or email to check
    :param password: password to validate against database

    :returns jwt encoded token
    """

    user = await crud.user.authenticate(
        identification=username,
        password=password
    )

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail='user inactive')

    access_token = create_access_token_jwt(user=user)

    return jsonable_encoder(access_token)

@router.get("/basic", tags=['Login Actions'])
async def login_basic(auth: BasicAuth = Depends(basic_auth)):
    """ Basic Authentication to set cookie """

    if not auth:
        response = Response(headers={"WWW-Authenticate": "Basic"}, status_code=401)
        return response

    #try:
    decoded = base64.b64decode(auth).decode("ascii")
    username, _, password = decoded.partition(":")

    access_token = await _validate_user(username=username, password=password)

    response = RedirectResponse(url="/docs")
    response = add_response_auth_cookie(response=response, access_token=access_token)

    return response

    #except:
    #    response = Response(headers={"WWW-Authenticate": "Basic"}, status_code=401)
    #    return response

@router.post('/token', response_model=Token, tags=['Login Actions'])
async def login_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """ OAuth2 compatible login form, provide user/password receive jwt """

    username = form_data.username
    password = form_data.password

    access_token = await _validate_user(username=username, password=password)
    response = JSONResponse({
        "access_token": access_token,
        "token_type": "bearer",
    })
    response = add_response_auth_cookie(response=response, access_token=access_token)

    return response
