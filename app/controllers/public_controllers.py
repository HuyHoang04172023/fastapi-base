from fastapi import APIRouter

from schemas.responses import GenericResponse
from services.base import BaseService
from utils.custom_log import LogRequest

public_router = APIRouter(route_class=LogRequest)


@public_router.get('/ping', response_model=GenericResponse)
async def check_health():
    return BaseService.custom_response()
