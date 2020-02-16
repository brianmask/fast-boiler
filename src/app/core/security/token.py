""" Token / Auth related functions """

from datetime import datetime, timedelta

#from fastapi.security import OAuth2PasswordBearer
import jwt
from starlette.responses import Response

from app.core import settings

from app.schema.auth import User

JWT_ALGORITHM = settings.JWT_ALGORITHM
JWT_SUBJECT = settings.JWT_SUBJECT


def create_access_token_jwt(
        *,
        user: User,
        expires_delta: timedelta = timedelta(seconds=settings.JWT_EXPIRATION_TIME)
) -> str:
    """ encode the data dict provided into jwt """

    now = datetime.utcnow()
    max_exp = settings.JWT_MAXIMUM_LIFETIME

    if expires_delta is not None:
        expire = datetime.utcnow() + expires_delta

    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    data = {
        'sub': user['id'],
        'iat': now,
        'exp': expire,
        'max_exp': max_exp,
        # Add whatever else here that I will use later
    }

    encoded_jwt = jwt.encode(data, settings.SECRET_KEY, algorithm=JWT_ALGORITHM)

    return encoded_jwt

def add_response_auth_cookie(*, response: Response, access_token: str) -> Response:
    """ Add auth cookie with provided token to the response object """

    max_age = settings.JWT_MAXIMUM_LIFETIME
    expires = settings.JWT_EXPIRATION_TIME

    response.set_cookie(
        "Authorization",
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=max_age,
        expires=expires,
    )

    return response
