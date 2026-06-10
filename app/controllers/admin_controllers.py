from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from middlewares.database import get_db_session
from middlewares.check_login import CheckLogin
from schemas.requests.search_input import SearchInput
from schemas.responses import (GenericResponse, ListUserOutput)
from services.base import BaseService
from services.user_service import UserService
from utils.custom_log import LogRequest

admin_router = APIRouter(route_class=LogRequest)


@admin_router.get('/user', response_model=GenericResponse[ListUserOutput])
async def get_list_users(base_data: Annotated[dict, Depends(CheckLogin())],
                         request_data: SearchInput = Depends(),
                         db_session: AsyncSession = Depends(get_db_session)):
    obj = await UserService.get_list_users(db_session, request_data)
    return BaseService.custom_response(obj)
