from pathlib import Path  # para o SQLite
from typing import Optional

import sqlalchemy as sa
from sqlalchemy.future.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from models.model_base import ModelBase

__engine: Optional[Engine] = None


def create_engine(sqlite: bool = False) -> Engine:
    """
    Function to configure the database engine
    """
    global __engine

    if __engine:
        return

    if sqlite:
        print("-- Using SQLite3")
        arquivo_db = "db/picoles.sqlite"
        folder = Path(arquivo_db).parent
        folder.mkdir(parents=True, exist_ok=True)
        conn_str = f"sqlite:///{arquivo_db}"
        __engine = sa.create_engine(
            conn_str, echo=False, connect_args={"check_same_thread": False}
        )
    else:
        print("-- Using postgres")
        conn_str = (
            "postgresql://postgres:postgres@localhost:5432/Udemy_SqlAlchemyEssencial"
        )
        __engine = sa.create_engine(conn_str, echo=False)

    return __engine


def create_session(use_sqlite: bool) -> Session:
    """
    Function to create the session to the database.
    """
    global __engine

    if not __engine:
        # create_engine()
        create_engine(sqlite=use_sqlite)

    session_builder = sessionmaker(__engine, expire_on_commit=False, class_=Session)

    session: Session = session_builder()
    return session


def create_tables(use_sqlite: bool) -> None:
    global __engine

    if not __engine:
        # create_engine()
        create_engine(sqlite=use_sqlite)

    import models.__all_models

    ModelBase.metadata.drop_all(__engine)
    ModelBase.metadata.create_all(__engine)
    print("Tables created.")
