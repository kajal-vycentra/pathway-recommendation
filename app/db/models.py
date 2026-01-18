import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, Text, ForeignKey, JSON, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.database import Base


class User(Base):
    """User model - represents a user taking the questionnaire."""
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    external_user_id = Column(String(255), unique=True, index=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    questionnaire_responses = relationship("QuestionnaireResponse", back_populates="user")
    recommendations = relationship("PathwayRecommendationRecord", back_populates="user")


class QuestionnaireResponse(Base):
    """Stores user's questionnaire answers."""
    __tablename__ = "questionnaire_responses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    entry_type = Column(String(50), nullable=False)  # 'yes_i_know' or 'no_im_new'
    answers = Column(JSON, nullable=False)  # Store all Q&A as JSON
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    # Relationships
    user = relationship("User", back_populates="questionnaire_responses")
    recommendation = relationship("PathwayRecommendationRecord", back_populates="questionnaire_response", uselist=False)


class PathwayRecommendationRecord(Base):
    """Stores AI-generated pathway recommendations."""
    __tablename__ = "pathway_recommendations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    questionnaire_response_id = Column(UUID(as_uuid=True), ForeignKey("questionnaire_responses.id"), nullable=False)

    # AI Recommendation Results
    recommended_pathway = Column(String(255), nullable=False, index=True)
    confidence = Column(Float, nullable=False)

    # Detected Profile
    spiritual_stage = Column(String(100), nullable=False)
    primary_need = Column(String(100), nullable=False)
    emotional_state = Column(String(100), nullable=False)

    # AI Response Details
    reasoning = Column(Text, nullable=False)
    next_step_message = Column(Text, nullable=False)

    # Raw AI response for debugging/audit
    raw_ai_response = Column(JSON, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    # Relationships
    user = relationship("User", back_populates="recommendations")
    questionnaire_response = relationship("QuestionnaireResponse", back_populates="recommendation")

    # Composite indexes for common query patterns
    __table_args__ = (
        Index('ix_recommendations_user_created', 'user_id', 'created_at'),
        Index('ix_recommendations_pathway_created', 'recommended_pathway', 'created_at'),
    )
