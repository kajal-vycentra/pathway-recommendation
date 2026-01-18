import re
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator, model_validator
from enum import Enum


class EntryType(str, Enum):
    """User entry type based on initial question."""
    YES_I_KNOW = "yes_i_know"
    NO_IM_NEW = "no_im_new"


class SpiritualStage(str, Enum):
    """Spiritual stage classification."""
    SEEKER = "seeker"
    NEW_BELIEVER = "new_believer"
    GROWING_BELIEVER = "growing_believer"
    STRUGGLING_BELIEVER = "struggling_believer"


class EmotionalState(str, Enum):
    """Emotional state classification."""
    ANXIOUS = "anxious"
    CONFUSED = "confused"
    CURIOUS = "curious"
    PAINFUL = "painful"
    OPEN = "open"
    HOPEFUL = "hopeful"
    DISTRESSED = "distressed"


class PrimaryNeed(str, Enum):
    """Primary spiritual need classification."""
    SALVATION = "salvation"
    PEACE = "peace"
    UNDERSTANDING = "understanding"
    PURPOSE = "purpose"
    HEALING = "healing"
    GROWTH = "growth"
    GUIDANCE = "guidance"


class QuestionnaireAnswer(BaseModel):
    """Single questionnaire answer."""
    question_number: int
    question: str
    answer: str | List[str]


class QuestionnaireSubmission(BaseModel):
    """User's questionnaire submission."""
    entry_type: EntryType
    answers: List[QuestionnaireAnswer]


class DetectedProfile(BaseModel):
    """User's detected spiritual profile."""
    spiritual_stage: str
    primary_need: str
    emotional_state: str


class PathwayRecommendation(BaseModel):
    """AI-generated pathway recommendation."""
    recommended_pathway: str
    confidence: float = Field(ge=0.0, le=1.0)
    detected_profile: DetectedProfile
    reasoning: str
    next_step_message: str


class RecommendationRequest(BaseModel):
    """Request model for pathway recommendation from your backend."""
    user_id: Optional[str] = Field(
        None,
        description="External user ID from your backend system (optional, will create new user if not provided)",
        max_length=255
    )
    entry_type: EntryType
    answers: Dict[str, str] = Field(
        ...,
        description="Dictionary of question numbers to answers (e.g., {'Q1': 'Very interested', 'Q2': 'Personal experiences'})"
    )

    @field_validator('user_id')
    @classmethod
    def validate_user_id(cls, v: Optional[str]) -> Optional[str]:
        """Validate user_id format."""
        if v is not None:
            # Remove leading/trailing whitespace
            v = v.strip()
            if len(v) == 0:
                return None
            # Check for potentially dangerous characters
            if any(char in v for char in ['<', '>', '"', "'", ';', '--']):
                raise ValueError("user_id contains invalid characters")
        return v

    @field_validator('answers')
    @classmethod
    def validate_answers(cls, v: Dict[str, str]) -> Dict[str, str]:
        """Validate answers dictionary."""
        # Import here to avoid circular import
        from config import settings

        if not v:
            raise ValueError("answers cannot be empty")

        if len(v) > settings.MAX_ANSWERS_COUNT:
            raise ValueError(f"Too many answers. Maximum allowed: {settings.MAX_ANSWERS_COUNT}")

        validated_answers = {}
        question_pattern = re.compile(r'^Q\d{1,2}$', re.IGNORECASE)

        for key, value in v.items():
            # Validate key format (Q1, Q2, etc.)
            if not question_pattern.match(key):
                raise ValueError(f"Invalid question key format: '{key}'. Expected format: Q1, Q2, etc.")

            # Normalize key to uppercase
            normalized_key = key.upper()

            # Validate value
            if not isinstance(value, str):
                raise ValueError(f"Answer for {key} must be a string")

            # Strip whitespace
            value = value.strip()

            if len(value) == 0:
                raise ValueError(f"Answer for {key} cannot be empty")

            if len(value) > settings.MAX_ANSWER_LENGTH:
                raise ValueError(f"Answer for {key} exceeds maximum length of {settings.MAX_ANSWER_LENGTH} characters")

            # Check for potentially malicious content
            if any(pattern in value.lower() for pattern in ['<script', 'javascript:', 'data:']):
                raise ValueError(f"Answer for {key} contains potentially unsafe content")

            validated_answers[normalized_key] = value

        return validated_answers

    @model_validator(mode='after')
    def validate_answer_count(self) -> 'RecommendationRequest':
        """Validate that there's at least one answer."""
        if not self.answers:
            raise ValueError("At least one answer is required")
        return self


class RecommendationResponse(BaseModel):
    """Response model for pathway recommendation."""
    success: bool
    data: Optional[PathwayRecommendation] = None
    user_id: Optional[str] = None
    recommendation_id: Optional[str] = None
    error: Optional[str] = None


class UserHistoryResponse(BaseModel):
    """Response for user's recommendation history."""
    success: bool
    user_id: str
    recommendations: List[Dict[str, Any]] = []
    error: Optional[str] = None
