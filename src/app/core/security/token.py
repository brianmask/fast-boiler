""" Token / Auth related functions """

from datetime import datetime, timedelta

from fastapi import HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt import PyJWTError
from starlette.status import HTTP_403_FORBIDDEN

from app import crud
from app.core import settings
from app.schema.auth import User
from app.schema.token import TokenPayload

JWT_ALGORITHM = "HS256"
JWT_SUBJECT = "access"

REUSABLE_OAUTH2 = OAuth2PasswordBearer(tokenUrl="/api/auth/login/jwt")

# Helpers

def create_access_token_jwt(*, data: dict, expires_delta: timedelta = None):
    """ encode the data dict provided into jwt """

    to_encode = data.copy()
    if expires_delta is not None:
        expire = datetime.utcnow() + expires_delta

    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire, "sub": JWT_SUBJECT})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=JWT_ALGORITHM)

    return encoded_jwt

# Depends

async def get_current_user_jwt(token: str = Security(REUSABLE_OAUTH2)):
    """ Reads jwt token and returns user """

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[JWT_ALGORITHM])
        token_data = TokenPayload(**payload)

    except PyJWTError:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )

    user = await crud.user.get(id=token_data.user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


async def get_current_active_user(current_user: User = Security(get_current_user_jwt)):
    """ user must be active """

    if not crud.user.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")

    return current_user


async def get_current_active_superuser(current_user: User = Security(get_current_user_jwt)):
    """ user must be superuser """

    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="The user doesn't have enough privileges")

    return current_user
