"""
Script to reset the database - drops all tables and recreates them.
Run this once to fix the UUID/Integer mismatch issue.
"""
import asyncio
from sqlalchemy import text
from database import async_engine
from db_models import Base


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
    print("\nDatabase reset complete! You can now run: python main.py")


if __name__ == "__main__":
    asyncio.run(reset_database())
