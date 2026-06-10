from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine

from utils.configs import project_settings

async_engine = create_async_engine(project_settings.get_db_url(to_string=True),
                                   echo=project_settings.DB_LOG, pool_pre_ping=True, query_cache_size=0)
async_session = async_sessionmaker(async_engine, autoflush=False, expire_on_commit=False, class_=AsyncSession)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        async with session.begin():
            try:
                yield session
                await session.commit()
            except Exception as ex:
                await session.rollback()
                raise
            finally:
                await session.close()
