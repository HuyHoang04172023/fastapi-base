from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from middlewares.database import get_db_session
from schemas.requests import (LoginInput, RegisterInput)
from schemas.responses import (GenericResponse, LoginOutput, UserOutput)
from services.auth_service import AuthService
from services.base import BaseService
from utils.custom_log import LogRequest

auth_router = APIRouter(route_class=LogRequest)


@auth_router.post('/register', response_model=GenericResponse)
async def register(request: Request, request_data: RegisterInput, db_session: AsyncSession = Depends(get_db_session)):
    obj = await AuthService.register(db_session, request_data)
    return BaseService.custom_response(UserOutput.model_validate(obj))


@auth_router.post('/login', response_model=GenericResponse[LoginOutput])
async def login(request: Request, request_data: LoginInput, db_session: AsyncSession = Depends(get_db_session)):
    obj = await AuthService.login(db_session, request_data)
    return BaseService.custom_response(LoginOutput.model_validate(obj))
