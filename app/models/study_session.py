from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.sql import func
from datetime import datetime
from app.models.card import Base


class StudySession(Base):
    """Study session model for tracking learning sessions"""
    __tablename__ = "study_sessions"

    id = Column(Integer, primary_key=True, index=True)
    deck_name = Column(String(100), nullable=True)
    session_type = Column(String(50), default="review")  # review, new, mixed
    max_cards = Column(Integer, default=20)
    cards_studied = Column(Integer, default=0)
    cards_correct = Column(Integer, default=0)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    ended_at = Column(DateTime(timezone=True), nullable=True)


class CardReview(Base):
    """Card review record within a session"""
    __tablename__ = "card_reviews"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("study_sessions.id"))
    card_id = Column(Integer, ForeignKey("cards.id"))
    quality = Column(Integer, nullable=False)
    response_time = Column(Float, default=0.0)
    reviewed_at = Column(DateTime(timezone=True), server_default=func.now())
