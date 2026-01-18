from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.db import get_db
from app.core.health import get_full_health_check

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health_check_simple():
    """Simple health check endpoint (public) - for load balancer probes."""
    return {
        "status": "ok",
        "version": settings.APP_VERSION
    }


@router.get("/health/detailed")
async def health_check_detailed(db: AsyncSession = Depends(get_db)):
    """
    Detailed health check endpoint with dependency status (public).

    Tests actual connectivity to:
    - PostgreSQL database
    - Redis cache
    - OpenRouter AI API

    Returns overall status and individual component health.
    """
    health_status = await get_full_health_check(db)
    return health_status
