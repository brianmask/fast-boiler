""" token based endpoints """

from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app import crud
from app.core import settings
from app.core.security.token import create_access_token_jwt
from app.schema.token import Token

router = APIRouter()

@router.post('/jwt', response_model=Token, tags=['login'])
async def login_jwt(form_data: OAuth2PasswordRequestForm = Depends()):
    """ OAuth2 compatible login form, provide user/password receive jwt """

    user = await crud.user.authenticate(
        identification=form_data.username,
        password=form_data.password
    )

    if not user:
        raise HTTPException(status_code=400, detail='incorrect credentials')

    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail='user inactive')

    token_expiration = timedelta(minutes=settings.JWT_EXPIRATION_TIME)

    jwt_token = create_access_token_jwt(
        data={'user_id': user['id']},
        expires_delta=token_expiration
    )

    return {
        "access_token": jwt_token,
        "token_type": "bearer",
    }
