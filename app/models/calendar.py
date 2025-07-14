from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Date
from sqlalchemy.sql import func
from datetime import datetime, date
from app.models.card import Base


class DailyActivity(Base):
    """Daily learning activity tracking"""
    __tablename__ = "daily_activities"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, unique=True, index=True)
    cards_studied = Column(Integer, default=0)
    cards_correct = Column(Integer, default=0)
    sessions_completed = Column(Integer, default=0)
    study_time_minutes = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class StudyReminder(Base):
    """Study reminder settings"""
    __tablename__ = "study_reminders"

    id = Column(Integer, primary_key=True, index=True)
    time = Column(String(5), nullable=False)  # HH:MM format
    enabled = Column(Boolean, default=True)
    deck_names = Column(Text, nullable=True)  # JSON array of deck names
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
