""" Depends for Basic Authentication """

from typing import Optional

from fastapi import HTTPException
from fastapi.security.base import SecurityBase
from fastapi.openapi.models import SecurityBase as SecurityBaseModel
from fastapi.security.utils import get_authorization_scheme_param

from starlette.status import HTTP_403_FORBIDDEN
from starlette.requests import Request


class BasicAuth(SecurityBase):
    """ mechanism to allow basic authentication """

    def __init__(self, scheme_name: str = None, auto_error: bool = True):
        self.scheme_name = scheme_name or self.__class__.__name__
        self.auto_error = auto_error
        self.model = SecurityBaseModel(type="http")

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "basic":
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN, detail="Not authenticated"
                )
            else:
                return None
        return param

BASIC_AUTH = BasicAuth(auto_error=False)
