from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine

from config import settings

# Convert sync URL to async URL for asyncpg
ASYNC_DATABASE_URL = settings.DATABASE_URL.replace(
    "postgresql://", "postgresql+asyncpg://"
)

# Async engine for production use (non-blocking)
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    pool_pre_ping=True,
    pool_size=20,          # Increased for concurrent requests
    max_overflow=40,       # Allow more connections during spikes
    pool_timeout=30,       # Wait up to 30s for connection
    pool_recycle=1800,     # Recycle connections every 30 minutes
    echo=settings.DEBUG,   # Log SQL in debug mode
)

# Async session factory
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Sync engine for migrations and init only
sync_engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)

# Base class for models
Base = declarative_base()


async def get_db() -> AsyncSession:
    """Async dependency to get database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db():
    """Initialize database tables asynchronously."""
    from db_models import Base
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


def init_db_sync():
    """Initialize database tables synchronously (for startup)."""
    from db_models import Base
    Base.metadata.create_all(bind=sync_engine)
