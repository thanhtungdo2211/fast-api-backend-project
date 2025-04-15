from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker

from configure import config

Base = declarative_base()

# Convert PostgreSQL URL to async format
ASYNC_URL_DATABASE = config.URL_DATABASE.replace('postgresql://', 'postgresql+asyncpg://')

# Create async engine
async_engine = create_async_engine(
    ASYNC_URL_DATABASE,
    pool_size=50,
    max_overflow=20, 
    pool_timeout=300,
    pool_pre_ping=True,
    echo=False  # Set to False in production
)

# Create async session maker
AsyncSessionLocal = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

# Async dependency for FastAPI
async def get_db() :
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()