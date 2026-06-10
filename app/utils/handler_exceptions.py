from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from services.base import BaseService
from utils.custom_exception import CustomException
from utils.custom_log import clog


def exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(CustomException)
    async def catch_custom_exception(request: Request, exc: CustomException):
        return BaseService.custom_response(errors=exc.payload, status_code=exc.status_code, message=exc.message)

    @app.exception_handler(StarletteHTTPException)
    async def catch_http_error(request: Request, exc: StarletteHTTPException):
        clog.opt(colors=True).error(f'<r>Response:</r>  {exc.status_code} - {exc.detail}')
        clog.info('======================= END   REQUEST =======================')
        return BaseService.custom_response(errors=exc.args, status_code=exc.status_code, message=exc.detail)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        clog.error(f"{exc.errors()}")
        clog.info('======================= END   REQUEST =======================')
        return BaseService.custom_response(errors=exc.errors(), status_code=400, message="Validate request failed")

    @app.exception_handler(Exception)
    async def other_exception_handler(request: Request, exc: Exception):
        clog.error(f"{exc.__str__()}")
        clog.info('======================= END   REQUEST =======================')
        return BaseService.custom_response(errors=exc.__str__(), status_code=500, message="Unknown error")