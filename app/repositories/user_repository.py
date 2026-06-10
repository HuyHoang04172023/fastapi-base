import sqlalchemy as sa
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User
from repositories.base import BaseRepository
from schemas.requests import LoginInput, SearchInput


class UserRepository(BaseRepository[User]):
    model_class = User

    @classmethod
    async def get_user_with_password(cls, session: AsyncSession, request_data: LoginInput) -> User | None:
        query = (select(cls.model_class)
                 .where(cls.model_class.email.__eq__(request_data.email.lower()))
                 .where(cls.model_class.password.__eq__(request_data.password))
                 .where(cls.model_class.is_active.__eq__(True)))
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def get_list(cls, session: AsyncSession, request_data: SearchInput) -> list:
        query = (select(cls.model_class)
                 .where(cls.model_class.is_active.__eq__(True))
                 .where(cls.model_class.is_admin.__eq__(False)))
        if request_data.keyword:
            query = query.where(cls.model_class.email.ilike(f"%{request_data.keyword}%") | cls.model_class.user_name.ilike(f"%{request_data.keyword}%"))
        total_query = query.with_only_columns(sa.func.count())
        total = await session.execute(total_query)
        query = query.offset(request_data.offset).limit(request_data.per_page)
        list_user = await session.execute(query)
        return [list_user.scalars().all(), total.scalar()]
