import os
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration settings."""

    # OpenRouter API Configuration
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1/chat/completions"
    AI_MODEL: str = "mistralai/mistral-7b-instruct"

    # Application Settings
    APP_NAME: str = "LogosReach Pathway Recommendation API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

    # API Authentication
    API_KEY: str = os.getenv("API_KEY", "")

    # PostgreSQL Database Configuration
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")

    # Redis Configuration (for shared caching across workers)
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    CACHE_TTL: int = int(os.getenv("CACHE_TTL", "3600"))  # 1 hour default

    # Rate Limiting Configuration
    RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))
    RATE_LIMIT_PER_HOUR: int = int(os.getenv("RATE_LIMIT_PER_HOUR", "500"))

    # AI API Retry Configuration
    AI_MAX_RETRIES: int = int(os.getenv("AI_MAX_RETRIES", "3"))
    AI_RETRY_DELAY: float = float(os.getenv("AI_RETRY_DELAY", "1.0"))

    # Request Validation
    MAX_ANSWER_LENGTH: int = int(os.getenv("MAX_ANSWER_LENGTH", "1000"))
    MAX_ANSWERS_COUNT: int = int(os.getenv("MAX_ANSWERS_COUNT", "20"))

    # Available Pathways
    PATHWAYS: List[dict] = [
        {
            "id": 1,
            "name": "Discovering Jesus",
            "duration": "7-10 days",
            "theme": "seeker, new to Christianity, not familiar with Jesus, curiosity about faith"
        },
        {
            "id": 2,
            "name": "New Believer Foundations",
            "duration": "14 days",
            "theme": "recently believed, needs basics of faith"
        },
        {
            "id": 3,
            "name": "Water Baptism",
            "duration": "7 days",
            "theme": "baptism, public declaration of faith"
        },
        {
            "id": 4,
            "name": "Growing in Prayer",
            "duration": "7 days",
            "theme": "learning to pray, anxiety, peace, trusting God"
        },
        {
            "id": 5,
            "name": "Understanding the Bible",
            "duration": "10-14 days",
            "theme": "confused about scripture, wants deeper context"
        },
        {
            "id": 6,
            "name": "Finding Purpose & Calling",
            "duration": "14-21 days",
            "theme": "purpose, calling, career direction, meaning in life"
        },
        {
            "id": 7,
            "name": "Marriage & Relationships",
            "duration": "14-21 days",
            "theme": "marriage issues, relationship struggles, family"
        },
        {
            "id": 8,
            "name": "Parenting with Faith",
            "duration": "14 days",
            "theme": "parenting, raising children, family faith"
        },
        {
            "id": 9,
            "name": "Overcoming Anxiety",
            "duration": "10-14 days",
            "theme": "worry, fear, need peace, anxiety, stress"
        },
        {
            "id": 10,
            "name": "Healing from Grief",
            "duration": "21-30 days",
            "theme": "loss, grief, mourning, bereavement"
        },
        {
            "id": 11,
            "name": "Financial Stewardship",
            "duration": "14-21 days",
            "theme": "finances, money management, stewardship, debt"
        },
        {
            "id": 12,
            "name": "Crisis Support",
            "duration": "Variable",
            "theme": "urgent help, hopelessness, fear, crisis, emergency"
        }
    ]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
