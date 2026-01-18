import logging
from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.api.dependencies import verify_api_key
from app.schemas import (
    RecommendationRequest,
    RecommendationResponse,
    UserHistoryResponse,
)
from app.services import RecommendationService
from app.core.rate_limit import rate_limit_default, rate_limit_strict

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Recommendations"])

# Initialize service
recommendation_service = RecommendationService()


@router.post("/recommend", response_model=RecommendationResponse)
@rate_limit_strict
async def recommend_pathway(
    request: Request,
    body: RecommendationRequest,
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
        body: RecommendationRequest with entry_type, answers, and optional user_id

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
            body, db
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
        logger.error(f"Recommendation error: {str(e)}")
        return RecommendationResponse(
            success=False,
            error=f"Failed to generate recommendation: {str(e)}"
        )


@router.get("/users/{user_id}/history", response_model=UserHistoryResponse)
@rate_limit_default
async def get_user_history(
    request: Request,
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
        UserHistoryResponse with list of past recommendations
    """
    try:
        history = await recommendation_service.get_user_history(db, user_id)
        return UserHistoryResponse(
            success=True,
            user_id=user_id,
            recommendations=history
        )
    except Exception as e:
        logger.error(f"History retrieval error: {str(e)}")
        return UserHistoryResponse(
            success=False,
            user_id=user_id,
            error=f"Failed to retrieve history: {str(e)}"
        )
