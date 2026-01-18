from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse

from config import settings


def get_api_key_or_ip(request: Request) -> str:
    """
    Get rate limit key based on API key (preferred) or IP address.

    This allows per-client rate limiting when API key is provided,
    falling back to IP-based limiting for unauthenticated requests.
    """
    api_key = request.headers.get("X-API-Key")
    if api_key:
        return f"api_key:{api_key[:16]}"  # Use first 16 chars of API key
    return f"ip:{get_remote_address(request)}"


# Create limiter instance with custom key function
limiter = Limiter(
    key_func=get_api_key_or_ip,
    default_limits=[f"{settings.RATE_LIMIT_PER_MINUTE}/minute"],
    storage_uri=settings.REDIS_URL if settings.REDIS_URL else None,
    strategy="fixed-window",
)


async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    """Custom handler for rate limit exceeded errors."""
    return JSONResponse(
        status_code=429,
        content={
            "success": False,
            "error": "Rate limit exceeded",
            "detail": str(exc.detail),
            "retry_after": exc.retry_after if hasattr(exc, 'retry_after') else 60
        },
        headers={
            "Retry-After": str(exc.retry_after if hasattr(exc, 'retry_after') else 60),
            "X-RateLimit-Limit": str(settings.RATE_LIMIT_PER_MINUTE),
        }
    )


def get_rate_limit_decorator(limit_string: str = None):
    """
    Get a rate limit decorator with custom limit.

    Args:
        limit_string: Rate limit string (e.g., "10/minute", "100/hour")
                     If None, uses default from settings.

    Returns:
        Rate limit decorator
    """
    if limit_string is None:
        limit_string = f"{settings.RATE_LIMIT_PER_MINUTE}/minute"
    return limiter.limit(limit_string)


# Pre-configured decorators for common use cases
rate_limit_default = limiter.limit(f"{settings.RATE_LIMIT_PER_MINUTE}/minute")
rate_limit_strict = limiter.limit("10/minute")  # For expensive operations
rate_limit_relaxed = limiter.limit(f"{settings.RATE_LIMIT_PER_HOUR}/hour")  # For read operations
