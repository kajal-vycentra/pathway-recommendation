import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from slowapi.errors import RateLimitExceeded

from app.config import settings
from app.db import async_engine, init_db
from app.core.cache import RedisCache
from app.core.rate_limit import limiter, rate_limit_exceeded_handler
from app.services import RecommendationService
from app.api.routes import (
    health_router,
    questions_router,
    pathways_router,
    recommendations_router,
)

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler with proper startup/shutdown."""
    # Startup
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")

    if not settings.OPENROUTER_API_KEY:
        logger.warning("OPENROUTER_API_KEY not set!")
    if not settings.API_KEY:
        logger.warning("API_KEY not set! API will reject all requests.")
    if not settings.DATABASE_URL:
        logger.error("DATABASE_URL not set!")

    # Initialize database tables
    logger.info("Initializing database...")
    await init_db()
    logger.info("Database initialized successfully!")

    # Initialize Redis connection
    logger.info("Initializing Redis cache...")
    await RedisCache.get_client()
    logger.info("Cache initialized!")

    yield

    # Shutdown - cleanup resources
    logger.info("Shutting down...")
    await RecommendationService.close_http_client()
    await RedisCache.close()
    if async_engine:
        await async_engine.dispose()
    logger.info("Cleanup complete!")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered spiritual pathway recommendation system - Scalable & Fast. Requires X-API-Key header for authentication.",
    lifespan=lifespan
)

# Add rate limiter to app state
app.state.limiter = limiter

# Add rate limit exceeded exception handler
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)

# CORS middleware - Configure for production
# TODO: Replace "*" with your actual frontend domains in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific origins in production: ["https://yourdomain.com"]
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["X-API-Key", "Content-Type", "Authorization"],
)

# Include routers
app.include_router(health_router)
app.include_router(questions_router)
app.include_router(pathways_router)
app.include_router(recommendations_router)


@app.get("/")
async def root():
    """Root endpoint with API info."""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "description": "AI-powered pathway recommendation system",
        "authentication": "Requires X-API-Key header for protected endpoints",
        "endpoints": {
            "public": {
                "GET /": "This info",
                "GET /health": "Simple health check",
                "GET /health/detailed": "Detailed health check with dependency status"
            },
            "protected": {
                "GET /questions/{entry_type}": "Get questionnaire questions",
                "GET /pathways": "Get all available pathways",
                "POST /recommend": "Get AI pathway recommendation",
                "GET /users/{user_id}/history": "Get user's recommendation history"
            }
        },
        "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        workers=1 if settings.DEBUG else 4
    )
