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

    if expires_delta is not None:
        expire = now + expires_delta

    else:
        expire = now + timedelta(minutes=15)

    data = {
        'sub': user['id'],
        'iat': now,
        'exp': expire,
        'max_exp': settings.JWT_MAXIMUM_LIFETIME,
        # Add whatever else here that I will use later
    }

    encoded_jwt = jwt.encode(data, settings.SECRET_KEY, algorithm=JWT_ALGORITHM)

    return encoded_jwt

def refresh_access_token_jwt(
        token: str,
        expires_delta: timedelta = timedelta(seconds=settings.JWT_EXPIRATION_TIME)
    ) -> str:
    """ refresh the provided token """

    decoded_jwt = jwt.decode(token, settings.SECRET_KEY, algorithms=JWT_ALGORITHM)

    refresh_jwt = decoded_jwt.copy()

    now = datetime.utcnow()

    iat = datetime.utcfromtimestamp(decoded_jwt.get('iat'))
    max_exp = iat + timedelta(seconds=decoded_jwt.get('max_exp'))

    new_exp = now + expires_delta

    if new_exp < max_exp:
        refresh_jwt['exp'] = new_exp

    else:
        refresh_jwt['exp'] = max_exp

    return jwt.encode(refresh_jwt, settings.SECRET_KEY, algorithm=JWT_ALGORITHM)

def add_response_auth_cookie(*, response: Response, access_token: str) -> Response:
    """ Add auth cookie with provided token to the response object """

    expires = settings.JWT_EXPIRATION_TIME
    secure = settings.SECURE_COOKIES

    response.set_cookie(
        "Authorization",
        value=f"Bearer {access_token}",
        httponly=True,
        expires=expires,
        secure=secure
    )

    return response
