from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker, AsyncEngine
from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.python_fastapi_project.domain.models.base import Base
from typing import Optional, AsyncGenerator
import os

# Global variables for engine and session maker
engine: Optional[AsyncEngine] = None  # Connection manager
AsyncSessionLocal: Optional[async_sessionmaker[AsyncSession]] = None  # Session factory

def setup_database_engine():
    """Initialize the database connection manager and session factory"""
    global engine, AsyncSessionLocal

    if engine is None:
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            raise ValueError("DATABASE_URL environment variable is not set")

        engine = create_async_engine(database_url, echo=True)
        AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

def get_session_factory() -> async_sessionmaker[AsyncSession]:
    """Get the session factory (ensures database is initialized first)"""
    if AsyncSessionLocal is None:
        setup_database_engine()

    if AsyncSessionLocal is None:
        raise RuntimeError("Failed to initialize database session maker")

    return AsyncSessionLocal

async def create_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Create a new database session for ORM operations"""
    session_factory = get_session_factory()
    async with session_factory() as session:
        yield session

@asynccontextmanager
async def database_lifespan(app: FastAPI):
    """Manage database lifecycle: setup on startup, cleanup on shutdown"""
    # Startup: Initialize database and create tables
    setup_database_engine()
    assert engine is not None

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield  # FastAPI runs here

    # Shutdown: Clean up database connections
    if engine:
        await engine.dispose()
