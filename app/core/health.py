import asyncio
import httpx
from typing import Dict, Any
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.core.cache import RedisCache


async def check_database(db: AsyncSession) -> Dict[str, Any]:
    """Check database connectivity and basic health."""
    try:
        # Execute a simple query to verify connection
        result = await db.execute(text("SELECT 1"))
        result.scalar()

        # Get connection pool stats if available
        return {
            "status": "healthy",
            "connected": True,
            "database": settings.DATABASE_URL.split("@")[-1].split("/")[-1] if "@" in settings.DATABASE_URL else "unknown"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "connected": False,
            "error": str(e)
        }


async def check_redis() -> Dict[str, Any]:
    """Check Redis connectivity."""
    return await RedisCache.health_check()


async def check_openrouter() -> Dict[str, Any]:
    """Check OpenRouter API connectivity."""
    if not settings.OPENROUTER_API_KEY:
        return {
            "status": "unconfigured",
            "connected": False,
            "error": "OPENROUTER_API_KEY not set"
        }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            # Use a lightweight endpoint to check connectivity
            response = await client.get(
                "https://openrouter.ai/api/v1/models",
                headers={
                    "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
                }
            )

            if response.status_code == 200:
                return {
                    "status": "healthy",
                    "connected": True,
                    "model": settings.AI_MODEL
                }
            elif response.status_code == 401:
                return {
                    "status": "unhealthy",
                    "connected": False,
                    "error": "Invalid API key"
                }
            else:
                return {
                    "status": "degraded",
                    "connected": True,
                    "status_code": response.status_code
                }
    except httpx.TimeoutException:
        return {
            "status": "unhealthy",
            "connected": False,
            "error": "Connection timeout"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "connected": False,
            "error": str(e)
        }


async def get_full_health_check(db: AsyncSession) -> Dict[str, Any]:
    """
    Perform comprehensive health check on all dependencies.

    Returns:
        Dict with overall status and individual component statuses.
    """
    # Run all checks concurrently
    db_check, redis_check, openrouter_check = await asyncio.gather(
        check_database(db),
        check_redis(),
        check_openrouter(),
        return_exceptions=True
    )

    # Handle any exceptions that occurred
    if isinstance(db_check, Exception):
        db_check = {"status": "error", "error": str(db_check)}
    if isinstance(redis_check, Exception):
        redis_check = {"status": "error", "error": str(redis_check)}
    if isinstance(openrouter_check, Exception):
        openrouter_check = {"status": "error", "error": str(openrouter_check)}

    # Determine overall status
    statuses = [
        db_check.get("status"),
        redis_check.get("status"),
        openrouter_check.get("status")
    ]

    if all(s == "healthy" for s in statuses):
        overall_status = "healthy"
    elif any(s == "unhealthy" or s == "error" for s in statuses):
        # Database is critical, others can be degraded
        if db_check.get("status") in ("unhealthy", "error"):
            overall_status = "unhealthy"
        else:
            overall_status = "degraded"
    else:
        overall_status = "degraded"

    return {
        "status": overall_status,
        "components": {
            "database": db_check,
            "redis": redis_check,
            "openrouter": openrouter_check
        },
        "config": {
            "api_key_configured": bool(settings.API_KEY),
            "debug_mode": settings.DEBUG,
            "rate_limit_per_minute": settings.RATE_LIMIT_PER_MINUTE
        }
    }
