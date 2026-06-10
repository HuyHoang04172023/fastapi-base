from sqlalchemy.ext.asyncio import AsyncSession

from models import User
from repositories import UserRepository
from schemas.requests import (LoginInput, RegisterInput)
from services.base import BaseService
from services.user_service import UserService
from utils.configs import project_settings
from utils.custom_exception import CustomException
from utils.security import generate_token


class AuthService(BaseService):

    @classmethod
    async def register(cls, db_session: AsyncSession, request_data: RegisterInput):
        new_user = await UserService.create_user(db_session, request_data)
        return new_user

    @classmethod
    async def login(cls, db_session: AsyncSession, request_data: LoginInput):
        obj = await UserRepository.get_user_with_password(db_session, request_data)
        if not obj:
            raise CustomException(404, "User not found.")
        response = {
            'id': obj.id,
            'email': obj.email,
            'access_token': generate_token(obj, project_settings.TOKEN_EXPIRE),
            'refresh_token': generate_token(obj, project_settings.TOKEN_REFRESH_EXPIRE),
        }
        return response
