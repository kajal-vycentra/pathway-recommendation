import json
import hashlib
import logging
from typing import Optional, Dict, Any
import redis.asyncio as redis
from cachetools import TTLCache

from app.config import settings

logger = logging.getLogger(__name__)


class RedisCache:
    """
    Redis-based cache for sharing cached responses across multiple workers.
    Falls back to in-memory cache if Redis is unavailable.
    """

    _redis_client: Optional[redis.Redis] = None
    _fallback_cache: TTLCache = TTLCache(maxsize=1000, ttl=settings.CACHE_TTL)
    _redis_available: bool = True

    @classmethod
    async def get_client(cls) -> Optional[redis.Redis]:
        """Get or create Redis client."""
        if cls._redis_client is None:
            try:
                cls._redis_client = redis.from_url(
                    settings.REDIS_URL,
                    encoding="utf-8",
                    decode_responses=True,
                    socket_connect_timeout=5,
                    socket_timeout=5,
                )
                # Test connection
                await cls._redis_client.ping()
                cls._redis_available = True
            except Exception as e:
                logger.warning(f"Redis connection failed, using fallback cache: {e}")
                cls._redis_available = False
                cls._redis_client = None
        return cls._redis_client

    @classmethod
    async def close(cls):
        """Close Redis connection."""
        if cls._redis_client is not None:
            await cls._redis_client.close()
            cls._redis_client = None

    @classmethod
    def generate_cache_key(cls, entry_type: str, answers: Dict[str, str]) -> str:
        """Generate a unique cache key from entry type and answers."""
        sorted_answers = json.dumps(
            {"entry_type": entry_type, "answers": dict(sorted(answers.items()))},
            sort_keys=True
        )
        return f"pathway_rec:{hashlib.md5(sorted_answers.encode()).hexdigest()}"

    @classmethod
    async def get(cls, key: str) -> Optional[Dict[str, Any]]:
        """Get value from cache (Redis or fallback)."""
        try:
            client = await cls.get_client()
            if client and cls._redis_available:
                value = await client.get(key)
                if value:
                    return json.loads(value)
        except Exception as e:
            logger.warning(f"Redis get error, using fallback: {e}")
            cls._redis_available = False

        # Fallback to in-memory cache
        return cls._fallback_cache.get(key)

    @classmethod
    async def set(cls, key: str, value: Dict[str, Any], ttl: Optional[int] = None) -> bool:
        """Set value in cache (Redis and fallback)."""
        ttl = ttl or settings.CACHE_TTL
        json_value = json.dumps(value)

        # Always set in fallback cache for local worker
        cls._fallback_cache[key] = value

        try:
            client = await cls.get_client()
            if client and cls._redis_available:
                await client.setex(key, ttl, json_value)
                return True
        except Exception as e:
            logger.warning(f"Redis set error: {e}")
            cls._redis_available = False

        return False

    @classmethod
    async def health_check(cls) -> Dict[str, Any]:
        """Check Redis connection health."""
        try:
            client = await cls.get_client()
            if client:
                await client.ping()
                info = await client.info("server")
                return {
                    "status": "healthy",
                    "redis_version": info.get("redis_version", "unknown"),
                    "connected": True
                }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "connected": False,
                "fallback_active": True
            }

        return {
            "status": "fallback",
            "connected": False,
            "fallback_active": True,
            "fallback_cache_size": len(cls._fallback_cache)
        }

    @classmethod
    def get_fallback_cache_size(cls) -> int:
        """Get the size of the fallback cache."""
        return len(cls._fallback_cache)
