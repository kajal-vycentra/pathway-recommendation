"""
Script to reset the database - drops all tables and recreates them.
Run this once to fix the UUID/Integer mismatch issue.

Usage:
    python -m scripts.reset_db

Or from the root directory:
    python scripts/reset_db.py
"""
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import asyncio
from sqlalchemy import text
from app.db.database import async_engine
from app.db.models import Base


async def reset_database():
    """Drop all tables and recreate with correct schema."""
    print("Connecting to database...")

    async with async_engine.begin() as conn:
        print("Dropping existing tables...")

        # Drop tables in correct order (respecting foreign keys)
        await conn.execute(text("DROP TABLE IF EXISTS pathway_enrollments CASCADE"))
        await conn.execute(text("DROP TABLE IF EXISTS pathway_recommendations CASCADE"))
        await conn.execute(text("DROP TABLE IF EXISTS questionnaire_responses CASCADE"))
        await conn.execute(text("DROP TABLE IF EXISTS users CASCADE"))

        print("Tables dropped successfully!")

        print("Creating tables with UUID schema...")
        await conn.run_sync(Base.metadata.create_all)

        print("Tables created successfully!")

    await async_engine.dispose()
    print("\nDatabase reset complete! You can now run: python run.py")


if __name__ == "__main__":
    asyncio.run(reset_database())
