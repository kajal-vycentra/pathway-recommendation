import json
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from database import get_db, init_db, async_engine
from auth import verify_api_key
from models import (
    RecommendationRequest,
    RecommendationResponse,
    UserHistoryResponse,
    EntryType,
)
from services.recommendation_service import RecommendationService


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler with proper startup/shutdown."""
    # Startup
    print(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    if not settings.OPENROUTER_API_KEY:
        print("WARNING: OPENROUTER_API_KEY not set!")
    if not settings.API_KEY:
        print("WARNING: API_KEY not set! API will reject all requests.")

    # Initialize database tables
    print("Initializing database...")
    await init_db()
    print("Database initialized successfully!")

    yield

    # Shutdown - cleanup resources
    print("Shutting down...")
    await RecommendationService.close_http_client()
    await async_engine.dispose()
    print("Cleanup complete!")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered spiritual pathway recommendation system - Scalable & Fast. Requires X-API-Key header for authentication.",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
recommendation_service = RecommendationService()


# ============== PUBLIC ENDPOINTS (No Auth Required) ==============

@app.get("/")
async def root():
    """Root endpoint with API info (public)."""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "authentication": "Required. Pass X-API-Key header for protected endpoints.",
        "features": [
            "Async database operations",
            "Connection pooling",
            "Response caching",
            "Multi-worker support",
            "API key authentication"
        ],
        "endpoints": {
            "public": {
                "root": "GET /",
                "health": "GET /health"
            },
            "protected": {
                "questions": "GET /questions/{entry_type}",
                "pathways": "GET /pathways",
                "recommend": "POST /recommend",
                "user_history": "GET /users/{user_id}/history"
            }
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint (public)."""
    return {
        "status": "healthy",
        "api_key_configured": bool(settings.API_KEY),
        "openrouter_configured": bool(settings.OPENROUTER_API_KEY),
        "database_configured": bool(settings.DATABASE_URL),
        "cache_size": len(RecommendationService._response_cache)
    }


# ============== PROTECTED ENDPOINTS (Auth Required) ==============

@app.get("/questions/{entry_type}")
async def get_questions(
    entry_type: EntryType,
    api_key: str = Depends(verify_api_key)
):
    """
    Get questionnaire questions based on entry type.

    Requires X-API-Key header.

    Args:
        entry_type: Either 'yes_i_know' or 'no_im_new'

    Returns:
        List of questions for the specified entry type
    """
    try:
        with open("questions.json", "r") as f:
            questions_data = json.load(f)

        flow_key = entry_type.value
        if flow_key not in questions_data["flows"]:
            raise HTTPException(status_code=404, detail=f"Flow '{flow_key}' not found")

        return {
            "entry_type": entry_type,
            "initial_question": questions_data["initial_question"],
            "questions": questions_data["flows"][flow_key]
        }
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Questions configuration not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid questions configuration")


@app.get("/pathways")
async def get_pathways(api_key: str = Depends(verify_api_key)):
    """
    Get all available pathways.

    Requires X-API-Key header.
    """
    return {
        "pathways": settings.PATHWAYS
    }


@app.post("/recommend", response_model=RecommendationResponse)
async def recommend_pathway(
    request: RecommendationRequest,
    db: AsyncSession = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    """
    Get AI-powered pathway recommendation based on questionnaire answers.

    Requires X-API-Key header.

    This endpoint is optimized for high concurrency:
    - Async database operations (non-blocking)
    - Connection pooling for AI API
    - Response caching for identical answer patterns

    Args:
        request: RecommendationRequest with entry_type, answers, and optional user_id

    Returns:
        RecommendationResponse with pathway recommendation and IDs for tracking

    Example request:
    ```
    Headers:
        X-API-Key: your_api_key_here

    Body:
    {
        "user_id": "external-user-123",
        "entry_type": "no_im_new",
        "answers": {
            "Q1": "Very interested",
            "Q2": "Personal experiences",
            "Q3": "No, not really",
            "Q4": "Not familiar at all",
            "Q5": "Seeking meaning or purpose",
            "Q6": "Very comfortable",
            "Q7": "Short simple lessons",
            "Q8": "Maybe / unsure",
            "Q9": "How to find peace",
            "Q10": "Very open"
        }
    }
    ```
    """
    try:
        recommendation, user_id, recommendation_id = await recommendation_service.get_recommendation(
            request, db
        )

        return RecommendationResponse(
            success=True,
            data=recommendation,
            user_id=user_id,
            recommendation_id=recommendation_id
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        return RecommendationResponse(
            success=False,
            error=f"Failed to generate recommendation: {str(e)}"
        )


@app.get("/users/{user_id}/history", response_model=UserHistoryResponse)
async def get_user_history(
    user_id: str,
    db: AsyncSession = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    """
    Get a user's recommendation history.

    Requires X-API-Key header.

    Args:
        user_id: External user ID

    Returns:
        List of past recommendations for the user
    """
    try:
        recommendations = await recommendation_service.get_user_history(db, user_id)

        return UserHistoryResponse(
            success=True,
            user_id=user_id,
            recommendations=recommendations
        )
    except Exception as e:
        return UserHistoryResponse(
            success=False,
            user_id=user_id,
            error=f"Failed to get history: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn

    # For production, use multiple workers:
    # uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        workers=1 if settings.DEBUG else 4  # Multiple workers in production
    )
