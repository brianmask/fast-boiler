""" refresh authentication cookies with every request """

from fastapi.encoders import jsonable_encoder
from starlette.middleware.base import BaseHTTPMiddleware

from app.core import settings
from app.core.security.backends.token import get_bearer
from app.core.security.token import refresh_access_token_jwt, add_response_auth_cookie

async def ensure_valid_path(current_path: str) -> bool:
    """ ensures the path is configured to allow auto refresh """

    paths_to_check = settings.NO_AUTO_REFRESH

    for path in paths_to_check:
        if path in current_path:
            return False

    return True


class AuthCookieRefresher(BaseHTTPMiddleware):
    """ creates new token with every request to refresh the expiration up to max """

    async def dispatch(self, request, call_next):
        """ check for token, refresh if exists """

        token = get_bearer(request)
        path = request.get('path')

        response = await call_next(request)
        valid_path = await ensure_valid_path(path)
        if token is not None and valid_path:
            if response.status_code >= 200 and response.status_code < 300:
                refresh_token = refresh_access_token_jwt(token.get('param'))

                if refresh_token is not None:
                    refresh_token = jsonable_encoder(refresh_token)

                    response = add_response_auth_cookie(
                        response=response, access_token=refresh_token
                    )
                    response.headers['access-token'] = refresh_token

        return response
