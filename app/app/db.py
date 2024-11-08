"""
Sets up postgres connection pool.
"""

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.config import settings

engine = create_async_engine(
    settings.sqlalchemy_database_url,  # type: ignore
    echo=False,
    connect_args={"server_settings": {"jit": "off"}},
)

async_session_factory = async_sessionmaker(engine, expire_on_commit=False)
