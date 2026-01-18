from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
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
        description="External user ID from your backend system (optional, will create new user if not provided)"
    )
    entry_type: EntryType
    answers: Dict[str, str] = Field(
        ...,
        description="Dictionary of question numbers to answers (e.g., {'Q1': 'Very interested', 'Q2': 'Personal experiences'})"
    )


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
