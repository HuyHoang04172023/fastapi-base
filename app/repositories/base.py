from typing import Any, Generic, Sequence, Type, TypeVar
import sqlalchemy as sa
from sqlalchemy import delete, func, insert, Row, RowMapping, Select, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.dml import ReturningDelete

from constants.sql_base_op import SqlBasicOp
from utils.custom_exception import CustomException
from utils.string_helpers import StringHelper

MODEL = TypeVar("MODEL", bound=Any)


class BaseRepository(Generic[MODEL]):
    model_class: Type[MODEL]

    @classmethod
    async def create(cls, session: AsyncSession, values: dict) -> MODEL:
        query = insert(cls.model_class).values(**values).returning(cls.model_class)
        result = await session.execute(query)
        return result.scalar_one()

    @classmethod
    async def update(cls, session: AsyncSession, values: dict, condition) -> MODEL:
        query = update(cls.model_class).where(condition).values(**values).returning(cls.model_class)
        result = await session.execute(query)
        return result.scalar_one()

    @classmethod
    async def insert_multi_in_trans(cls, session: AsyncSession, list_obj: list[MODEL]):
        try:
            session.add_all(list_obj)
            await session.commit()
        except Exception as ex:
            await session.rollback()
            raise CustomException(500, str(ex))

    @classmethod
    async def generate_op_sql(cls, column, value, op, eq_w_case_insensitive=False):
        if isinstance(column, str):
            column = getattr(cls.model_class, column, None)
        if not column:
            raise CustomException(400, message='[{}] is not column in table [{}]'.format(column, cls.model_class.__table__))
        try:
            attr = list(filter(lambda e: hasattr(column, e % op), ['%s', '%s_', '__%s__']))[0] % op
        except IndexError:
            raise CustomException(400, message='filter[{}] operator({}) invalid'.format(column, op))
        if attr == 'like' or attr == 'ilike':
            search_value = StringHelper.escape_special_character_in_like_filter(value=value)
            value = search_value if eq_w_case_insensitive else "%" + search_value + "%"
        filter_obj = getattr(column, attr)(value)
        if filter_obj is NotImplemented:
            raise CustomException(message='Can\'t generate filter from column {}'.format(column))
        return filter_obj

    @classmethod
    async def get_by_column(cls, session: AsyncSession, column, value, op=SqlBasicOp.EQ.value,
                            is_many=False, options=None) -> Any:
        filter_obj = await cls.generate_op_sql(column, value, op)
        query = select(cls.model_class).where(filter_obj)
        if options:
            query = query.options(options)
        result = await session.execute(query)
        if is_many:
            return result.scalars().all()
        else:
            return result.scalar_one_or_none()

    @classmethod
    async def get_all_per_column(cls, session: AsyncSession, column, order=None,
                                 with_primary_key=True) -> Sequence[Row | RowMapping | Any]:
        if isinstance(column, str):
            column = getattr(cls.model_class, column, None)
        if with_primary_key:
            query = select(cls.model_class.__table__.primary_key, column).distinct()
        else:
            query = select(column).distinct()
        if order:
            query = query.order_by(order)
        else:
            query = query.order_by(column)
        res = await session.scalars(query)
        return res.all()

    @classmethod
    async def delete_by_column(cls, session: AsyncSession, column, value, op=SqlBasicOp.EQ.value,
                               in_transaction=True) -> ReturningDelete[Any]:
        filter_obj = await cls.generate_op_sql(column, value, op)
        obj = delete(cls.model_class).where(filter_obj).returning()
        if not in_transaction:
            await session.commit()
        return obj

    @classmethod
    async def count(cls, session: AsyncSession, stmt: Select) -> int:
        return (await session.execute(select(func.count()).select_from(stmt.subquery()))).scalar_one()
