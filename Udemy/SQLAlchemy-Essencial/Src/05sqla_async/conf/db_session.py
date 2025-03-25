from pathlib import Path
from typing import Optional

import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from models.model_base import ModelBase

__async_engine: Optional[AsyncEngine] = None


def create_engine(sqlite: bool = False) -> AsyncEngine:
    """
    Function to configure the database engine
    """
    global __async_engine

    if __async_engine:
        return __async_engine

    if sqlite:
        arquivo_db = "db/picoles.sqlite"
        folder = Path(arquivo_db).parent
        folder.mkdir(parents=True, exist_ok=True)
        conn_str = f"sqlite+aiosqlite:///{arquivo_db}"
        __async_engine = create_async_engine(
            url=conn_str, echo=False, connect_args={"check_same_thread": False}
        )
    else:
        conn_str = "postgresql+asyncpg://postgres:postgres@localhost:5432/Udemy_SqlAlchemyEssencial"
        __async_engine = create_async_engine(url=conn_str, echo=False)
    return __async_engine


def create_session(use_sqlite: bool) -> AsyncSession:
    """
    Function to create the session to the database.
    """
    global __async_engine

    if not __async_engine:
        create_engine(use_sqlite)

    __async_session = sessionmaker(
        __async_engine, expire_on_commit=False, class_=AsyncSession
    )

    session: AsyncSession = __async_session()
    return session


async def create_tables(use_sqlite: bool) -> None:
    global __async_engine

    if not __async_engine:
        create_engine(use_sqlite)

    import models.__all_models

    async with __async_engine.begin() as conn:
        await conn.run_sync(ModelBase.metadata.drop_all)
        await conn.run_sync(ModelBase.metadata.create_all)
