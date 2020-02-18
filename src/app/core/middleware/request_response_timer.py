""" time the request / response cycle and add to response header """

import time

from starlette.middleware.base import BaseHTTPMiddleware


class RequestResponseTimer(BaseHTTPMiddleware):
    """ add system time spent on api call to header """

    async def dispatch(self, request, call_next):
        """ add system time spent on api call to header """

        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers['X-Process-Time'] = str(process_time)
        return response
