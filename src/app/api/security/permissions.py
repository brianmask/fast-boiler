""" Permissions (Depends) """

from fastapi import HTTPException, Security
import jwt
from jwt import PyJWTError
from starlette.status import HTTP_403_FORBIDDEN

from app import crud
from app.core import settings
from app.core.security.backends import OAuth2PasswordBearerCookie
from app.schema.auth import User
from app.schema.token import TokenPayload

REUSABLE_OAUTH2 = OAuth2PasswordBearerCookie(tokenUrl="/api/auth/login/token")
JWT_ALGORITHM = settings.JWT_ALGORITHM

async def get_token_payload_no_verify(token: str = Security(REUSABLE_OAUTH2)):
    """ Reads jwt token and returns user from payload !! does not verify the signature !!

    adding a variable to get_token_payload similar to verify: bool = True will expose
    the variable to api and document the option in swagger.  We don't want to let a user
    control if the token was verified or not.

    :param token: the jwt to decode
    :param verify: cryptography verification of the token
    """

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[JWT_ALGORITHM], verify=False)
        token_data = TokenPayload(**payload)

    except PyJWTError:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )

    return token_data

async def get_token_payload(token: str = Security(REUSABLE_OAUTH2)):
    """ Reads jwt token and returns user from payload

    :param token: the jwt to decode
    :param verify: cryptography verification of the token
    """

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[JWT_ALGORITHM])
        token_data = TokenPayload(**payload)

    except PyJWTError:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )

    return token_data

async def get_current_user(token_data: TokenPayload = Security(get_token_payload)):
    """ Reads jwt token and returns user """

    user = await crud.user.get(id=token_data.sub)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

async def get_current_active_user(current_user: User = Security(get_current_user)):
    """ user must be active """

    if not crud.user.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")

    return current_user


async def get_current_active_superuser(current_user: User = Security(get_current_active_user)):
    """ user must be superuser """

    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="The user doesn't have enough privileges")

    return current_user
