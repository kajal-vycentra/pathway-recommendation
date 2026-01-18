"""
Entry point for running the application.

Usage:
    python run.py                    # Development mode (single worker, auto-reload)
    python run.py --production       # Production mode (4 workers, no reload)

Or use uvicorn directly:
    uvicorn app.main:app --reload    # Development
    uvicorn app.main:app --workers 4 # Production
"""

import sys
import uvicorn

from app.config import settings


def main():
    """Run the FastAPI application."""
    # Check for production flag
    production = "--production" in sys.argv or "-p" in sys.argv

    if production or not settings.DEBUG:
        # Production mode
        print("Starting in PRODUCTION mode...")
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=8000,
            workers=4,
            log_level="info"
        )
    else:
        # Development mode
        print("Starting in DEVELOPMENT mode...")
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="debug"
        )


if __name__ == "__main__":
    main()
