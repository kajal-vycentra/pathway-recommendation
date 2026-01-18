from fastapi import APIRouter, Depends, Request

from app.config import settings
from app.api.dependencies import verify_api_key
from app.core.rate_limit import rate_limit_default

router = APIRouter(tags=["Pathways"])


@router.get("/pathways")
@rate_limit_default
async def get_pathways(request: Request, api_key: str = Depends(verify_api_key)):
    """
    Get all available pathways.

    Requires X-API-Key header.
    """
    return {
        "pathways": settings.PATHWAYS
    }
