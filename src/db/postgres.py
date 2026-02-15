from src.db import DatabaseAdapter
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
import logging
from typing import Any
from sqlalchemy import insert
from contextlib import asynccontextmanager
from uuid import UUID


class Postgres(DatabaseAdapter):
    def __init__(self, settings):
        self.settings = settings
        self.async_engine = None
        self.async_session_maker = None
        self.POSTGRES_URL = f"postgresql+asyncpg://{self.settings.postgres_user}:{self.settings.postgres_password}@{self.settings.postgres_service}:{self.settings.postgres_port}/{self.settings.postgres_db}"

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()

    async def connect(self):
        # Add search_path to use the active schema (test)
        connect_args = {
            "server_settings": {"search_path": f"{self.settings.active_schema}"}
        }

        self.async_engine = create_async_engine(
            self.POSTGRES_URL,
            pool_size=100,
            max_overflow=10,
            pool_pre_ping=True,
            pool_recycle=3600,
            echo=False,
            connect_args=connect_args,
        )

        self.async_session_maker = async_sessionmaker(
            self.async_engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False,
        )

        logging.info("Connected to PostgreSQL database")

    async def disconnect(self):
        if self.async_engine:
            await self.async_engine.dispose()
            logging.info("Disconnected from PostgreSQL database")

    @asynccontextmanager
    async def get_session(self, query_type: str):
        session = self.async_session_maker()
        try:
            yield session
            await session.commit()
        except Exception as e:
            logging.error(f"Error during {query_type} session: {e}")
            await session.rollback()
            raise e
        finally:
            await session.close()

    async def execute_query(self, query, params=None):
        async with self.get_session("row query") as session:
            result = await session.execute(query)

            # Use mappings() to get RowMapping objects, then convert to plain dicts
            mapped_rows = result.mappings().all()
            converted_rows = []
            for row in mapped_rows:
                row_dict = dict(row)
                # Check if any value is a SQLAlchemy ORM object and extract its attributes
                for key, value in row_dict.items():
                    if hasattr(value, '__mapper__'):  # It's a SQLAlchemy ORM object
                        # Convert ORM object to dict by extracting column values
                        orm_dict = {}
                        for col in value.__mapper__.columns:
                            col_value = getattr(value, col.name)
                            # Convert UUID objects to strings
                            if isinstance(col_value, UUID):
                                orm_dict[col.name] = str(col_value)
                            else:
                                orm_dict[col.name] = col_value
                        row_dict = orm_dict
                        break
                converted_rows.append(row_dict)
            return converted_rows

    async def execute_count_query(self, query):
        async with self.get_session("count query") as session:
            return await session.scalar(query)

    async def insert_rows(
        self, table_model: Any, query_type: str, rows: list[Any], returning: list[Any]
    ):
        async with self.get_session(query_type) as session:
            stmt = insert(table_model).values(rows).returning(*returning)
            result = await session.execute(stmt)
            return [dict(row) for row in result.mappings().all()]
