import time
from typing import Callable

from fastapi import Request, Response
from fastapi.routing import APIRoute
from loguru import logger as clog

clog.remove()
clog.add("zlogs/log_{time:YYYY_MM_DD}.log", rotation='10 MB', retention="30 days", backtrace=True, diagnose=True)


class LogRequest(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            clog.info('======================= START REQUEST =======================')
            clog.opt(colors=True).info(f"<g>Request URL</g>: [{request.method}] {request.url}")
            clog.opt(colors=True).info(f"<g>Request header</g>: {request.headers}")
            body = await request.body()
            clog.opt(colors=True).info(f"<g>Request body</g>: {body}")
            before = time.time()
            response: Response = await original_route_handler(request)
            duration = time.time() - before
            clog.opt(colors=True).info(f'<g>Response code</g>: {response.status_code}')
            clog.opt(colors=True).info(f'<g>Response data</g>: {response.body}')
            clog.opt(colors=True).info(f'<r>Time execute</r>: {duration}')
            clog.info('======================= END   REQUEST =======================')
            return response

        return custom_route_handler
