from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class CardBase(BaseModel):
    """Base card schema with common fields"""
    front: str = Field(..., min_length=1, max_length=2000, description="Question or prompt side of the card")
    back: str = Field(..., min_length=1, max_length=2000, description="Answer side of the card")
    deck_name: str = Field(default="default", max_length=100, description="Name of the deck this card belongs to")


class CardCreate(CardBase):
    """Schema for creating a new card"""
    pass


class CardUpdate(BaseModel):
    """Schema for updating an existing card"""
    front: Optional[str] = Field(None, min_length=1, max_length=2000)
    back: Optional[str] = Field(None, min_length=1, max_length=2000)
    deck_name: Optional[str] = Field(None, max_length=100)


class CardResponse(CardBase):
    """Schema for card responses"""
    id: int
    ease_factor: float
    interval: int
    repetitions: int
    created_at: datetime
    updated_at: Optional[datetime]
    next_review: datetime
    last_reviewed: Optional[datetime]

    class Config:
        from_attributes = True


class CardReview(BaseModel):
    """Schema for reviewing a card"""
    quality: int = Field(..., ge=0, le=5, description="Quality of recall (0-5, where 5 is perfect recall)")
    response_time: float = Field(default=0.0, ge=0, description="Response time in seconds")


class CardListResponse(BaseModel):
    """Schema for paginated card list responses"""
    cards: list[CardResponse]
    total: int
    page: int
    size: int
    pages: int


class StudySessionCreate(BaseModel):
    """Schema for creating a study session"""
    deck_name: Optional[str] = None
    session_type: str = Field(default="review", pattern="^(review|new|mixed)$")
    max_cards: int = Field(default=20, ge=1, le=100)


class StudySessionResponse(BaseModel):
    """Schema for study session responses"""
    id: int
    deck_name: Optional[str]
    session_type: str
    max_cards: int
    cards_studied: int
    cards_correct: int
    started_at: datetime
    ended_at: Optional[datetime]
    session_complete: bool = False

    class Config:
        from_attributes = True


class SessionReview(BaseModel):
    """Schema for reviewing a card within a session"""
    card_id: int
    quality: int = Field(..., ge=0, le=5)
    response_time: float = Field(default=0.0, ge=0)


class NextCardResponse(BaseModel):
    """Schema for next card in session"""
    card: Optional[CardResponse]
    session_complete: bool


class StudyStatsResponse(BaseModel):
    """Schema for study statistics"""
    total_sessions: int
    total_cards_studied: int
    average_accuracy: float


class DailyDueCountResponse(BaseModel):
    """Schema for daily due card count"""
    date: str
    due_count: int
    by_deck: dict[str, int]


class WeeklyProgressResponse(BaseModel):
    """Schema for weekly progress"""
    start_date: str
    end_date: str
    daily_stats: list[dict]


class LearningStreakResponse(BaseModel):
    """Schema for learning streak"""
    current_streak: int
    longest_streak: int
    last_study_date: Optional[str]


class MonthlyHeatmapResponse(BaseModel):
    """Schema for monthly activity heatmap"""
    year_month: str
    activity_data: list[dict]


class DeckProgressResponse(BaseModel):
    """Schema for deck progress over time"""
    deck_name: str
    period_days: int
    progress_data: list[dict]


class ReminderCreate(BaseModel):
    """Schema for creating study reminders"""
    time: str = Field(..., pattern="^([01]?[0-9]|2[0-3]):[0-5][0-9]$")
    enabled: bool = True
    deck_names: list[str] = []


class ReminderResponse(BaseModel):
    """Schema for reminder responses"""
    id: int
    time: str
    enabled: bool
    deck_names: list[str]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class UpcomingReviewsResponse(BaseModel):
    """Schema for upcoming reviews"""
    period_days: int
    upcoming_reviews: list[dict]
