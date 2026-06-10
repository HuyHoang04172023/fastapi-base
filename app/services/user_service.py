from sqlalchemy.ext.asyncio import AsyncSession

from repositories import UserRepository
from schemas.requests import RegisterInput
from schemas.requests.search_input import SearchInput
from schemas.responses import ListUserOutput
from services.base import BaseService
from utils.custom_exception import CustomException
from utils.security import hash_password


class UserService(BaseService):

    @classmethod
    async def get_list_users(cls, db_session: AsyncSession, request_data: SearchInput):
        list_users, total = await UserRepository.get_list(db_session, request_data)
        obj = ListUserOutput(list=list_users, total=total).model_dump()
        return obj

    @classmethod
    async def create_user(cls, db_session: AsyncSession, request_data: RegisterInput):
        obj = await UserRepository.get_by_column(db_session, 'email', request_data.email.lower())
        if obj:
            raise CustomException(400, "Email existed.")
        new_user = await UserRepository.create(db_session, {
            'email': request_data.email.lower(),
            'password': hash_password(request_data.password),
            'user_name': request_data.user_name.lower(),
        })
        return new_user
