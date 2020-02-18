""" OAuth2 Compatible Token/Cookie Authentication """

from typing import Dict, Optional

from fastapi import HTTPException
from fastapi.security import  OAuth2
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel

from starlette.status import HTTP_403_FORBIDDEN
from starlette.requests import Request

def get_bearer(request: Request) -> Optional[Dict]:
    """ attempts to read headers or cookies for authorization 'bearer' token """

    header_authorization: str = request.headers.get("Authorization")
    cookie_authorization: str = request.cookies.get("Authorization")

    header_scheme, header_param = get_authorization_scheme_param(
        header_authorization
    )
    cookie_scheme, cookie_param = get_authorization_scheme_param(
        cookie_authorization
    )

    if header_scheme.lower() == "bearer":
        authorization = True
        scheme = header_scheme
        param = header_param

    elif cookie_scheme.lower() == "bearer":
        authorization = True
        scheme = cookie_scheme
        param = cookie_param

    else:
        authorization = None

    if authorization:
        return {'scheme': scheme, 'param': param}

class OAuth2PasswordBearerCookie(OAuth2):
    """ reads token from header of cookie for auth

    Defaults to header authentication, reading from cookie when header
    was not provided
    """
    def __init__(
            self,
            tokenUrl: str,
            scheme_name: str = None,
            scopes: dict = None,
            auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}

        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        """ check for bearer token.  raise 403 if auto_error is True """

        data = get_bearer(request)

        if not data:
            if self.auto_error:
                raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not authenticated")
            else:
                return None

        return data.get('param')

OAUTH2_SCHEME = OAuth2PasswordBearerCookie(tokenUrl="/api/auth/login/token")
