"""API route modules."""

from app.api.routes.health import router as health_router
from app.api.routes.questions import router as questions_router
from app.api.routes.pathways import router as pathways_router
from app.api.routes.recommendations import router as recommendations_router

__all__ = [
    "health_router",
    "questions_router",
    "pathways_router",
    "recommendations_router",
]
