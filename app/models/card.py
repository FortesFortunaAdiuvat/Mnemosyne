from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime
from typing import Optional

Base = declarative_base()


class Card(Base):
    """
    Card model for spaced repetition learning system
    """
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    front = Column(Text, nullable=False)  # Question/prompt side
    back = Column(Text, nullable=False)   # Answer side
    deck_name = Column(String(100), nullable=False, default="default")
    
    # Spaced repetition algorithm fields
    ease_factor = Column(Float, default=2.5)  # How easy the card is (2.5 is default)
    interval = Column(Integer, default=1)     # Days until next review
    repetitions = Column(Integer, default=0)  # Number of successful repetitions
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    next_review = Column(DateTime(timezone=True), default=func.now())
    last_reviewed = Column(DateTime(timezone=True), nullable=True)

    def __repr__(self):
        return f"<Card(id={self.id}, front='{self.front[:50]}...', deck='{self.deck_name}')>"
