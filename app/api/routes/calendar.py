from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime, date, timedelta
import json
from app.core.database import get_db
from app.models.card import Card
from app.models.study_session import StudySession
from app.models.calendar import DailyActivity, StudyReminder
from app.models.schemas import (
    DailyDueCountResponse, WeeklyProgressResponse, LearningStreakResponse,
    MonthlyHeatmapResponse, DeckProgressResponse, ReminderCreate, 
    ReminderResponse, UpcomingReviewsResponse
)

router = APIRouter()


@router.get("/due-count", response_model=DailyDueCountResponse)
def get_daily_due_count(date: str, db: Session = Depends(get_db)):
    """Get count of due cards for a specific date"""
    target_date = datetime.fromisoformat(date).date()
    target_datetime = datetime.combine(target_date, datetime.min.time())
    
    # Get due cards for the date
    due_cards = db.query(Card).filter(Card.next_review <= target_datetime).all()
    
    # Count by deck
    by_deck = {}
    for card in due_cards:
        deck = card.deck_name or "default"
        by_deck[deck] = by_deck.get(deck, 0) + 1
    
    return DailyDueCountResponse(
        date=date,
        due_count=len(due_cards),
        by_deck=by_deck
    )


@router.get("/weekly-progress", response_model=WeeklyProgressResponse)
def get_weekly_progress(start_date: str, db: Session = Depends(get_db)):
    """Get weekly learning progress"""
    start = datetime.fromisoformat(start_date).date()
    end = start + timedelta(days=6)
    
    daily_stats = []
    for i in range(7):
        current_date = start + timedelta(days=i)
        sessions = db.query(StudySession).filter(
            func.date(StudySession.started_at) == current_date
        ).all()
        
        total_studied = sum(s.cards_studied for s in sessions)
        total_correct = sum(s.cards_correct for s in sessions)
        accuracy = (total_correct / total_studied * 100) if total_studied > 0 else 0
        
        daily_stats.append({
            "date": current_date.isoformat(),
            "sessions": len(sessions),
            "cards_studied": total_studied,
            "accuracy": round(accuracy, 1)
        })
    
    return WeeklyProgressResponse(
        start_date=start.isoformat(),
        end_date=end.isoformat(),
        daily_stats=daily_stats
    )


@router.get("/streak", response_model=LearningStreakResponse)
def get_learning_streak(db: Session = Depends(get_db)):
    """Get current learning streak"""
    # Get all study dates in descending order
    study_dates = db.query(func.date(StudySession.started_at).label('study_date')).distinct().order_by(func.date(StudySession.started_at).desc()).all()
    
    if not study_dates:
        return LearningStreakResponse(current_streak=0, longest_streak=0, last_study_date=None)
    
    dates = [d.study_date for d in study_dates]
    current_streak = 0
    longest_streak = 0
    temp_streak = 1
    
    # Calculate current streak
    today = date.today()
    if dates[0] == today or dates[0] == today - timedelta(days=1):
        current_streak = 1
        for i in range(1, len(dates)):
            if dates[i-1] - dates[i] == timedelta(days=1):
                current_streak += 1
            else:
                break
    
    # Calculate longest streak
    for i in range(1, len(dates)):
        if dates[i-1] - dates[i] == timedelta(days=1):
            temp_streak += 1
        else:
            longest_streak = max(longest_streak, temp_streak)
            temp_streak = 1
    longest_streak = max(longest_streak, temp_streak)
    
    return LearningStreakResponse(
        current_streak=current_streak,
        longest_streak=longest_streak,
        last_study_date=str(dates[0]) if dates else None
    )


@router.get("/heatmap", response_model=MonthlyHeatmapResponse)
def get_monthly_heatmap(year_month: str, db: Session = Depends(get_db)):
    """Get monthly activity heatmap data"""
    year, month = map(int, year_month.split('-'))
    start_date = date(year, month, 1)
    
    # Get next month's first day
    if month == 12:
        end_date = date(year + 1, 1, 1)
    else:
        end_date = date(year, month + 1, 1)
    
    # Get daily activity data
    activities = db.query(
        func.date(StudySession.started_at).label('date'),
        func.count(StudySession.id).label('sessions'),
        func.sum(StudySession.cards_studied).label('cards_studied')
    ).filter(
        and_(
            func.date(StudySession.started_at) >= start_date,
            func.date(StudySession.started_at) < end_date
        )
    ).group_by(func.date(StudySession.started_at)).all()
    
    activity_data = []
    for activity in activities:
        activity_data.append({
            "date": str(activity.date),
            "sessions": activity.sessions,
            "cards_studied": activity.cards_studied or 0,
            "intensity": min(activity.cards_studied or 0, 50) / 50  # Normalize to 0-1
        })
    
    return MonthlyHeatmapResponse(
        year_month=year_month,
        activity_data=activity_data
    )


@router.get("/deck-progress", response_model=DeckProgressResponse)
def get_deck_progress(deck_name: str, days: int = 30, db: Session = Depends(get_db)):
    """Get deck progress over time"""
    end_date = date.today()
    start_date = end_date - timedelta(days=days-1)
    
    # Get daily progress for the deck
    progress_data = []
    for i in range(days):
        current_date = start_date + timedelta(days=i)
        
        # Count cards in deck
        total_cards = db.query(Card).filter(Card.deck_name == deck_name).count()
        
        # Count cards reviewed on this date
        reviewed_cards = db.query(Card).filter(
            and_(
                Card.deck_name == deck_name,
                func.date(Card.last_reviewed) == current_date
            )
        ).count()
        
        progress_data.append({
            "date": current_date.isoformat(),
            "total_cards": total_cards,
            "reviewed_cards": reviewed_cards,
            "progress_percent": (reviewed_cards / total_cards * 100) if total_cards > 0 else 0
        })
    
    return DeckProgressResponse(
        deck_name=deck_name,
        period_days=days,
        progress_data=progress_data
    )


@router.post("/reminder", response_model=ReminderResponse, status_code=status.HTTP_201_CREATED)
def create_reminder(reminder: ReminderCreate, db: Session = Depends(get_db)):
    """Create a study reminder"""
    db_reminder = StudyReminder(
        time=reminder.time,
        enabled=reminder.enabled,
        deck_names=json.dumps(reminder.deck_names)
    )
    db.add(db_reminder)
    db.commit()
    db.refresh(db_reminder)
    
    reminder_dict = db_reminder.__dict__.copy()
    reminder_dict['deck_names'] = json.loads(db_reminder.deck_names or "[]")
    return ReminderResponse(**reminder_dict)


@router.get("/upcoming", response_model=UpcomingReviewsResponse)
def get_upcoming_reviews(days: int = 7, db: Session = Depends(get_db)):
    """Get upcoming review schedule"""
    start_date = datetime.now()
    end_date = start_date + timedelta(days=days)
    
    # Get cards due in the period
    upcoming_cards = db.query(Card).filter(
        and_(
            Card.next_review >= start_date,
            Card.next_review <= end_date
        )
    ).order_by(Card.next_review).all()
    
    # Group by date
    upcoming_reviews = []
    current_date = None
    daily_cards = []
    
    for card in upcoming_cards:
        review_date = card.next_review.date()
        
        if current_date != review_date:
            if current_date is not None:
                upcoming_reviews.append({
                    "date": current_date.isoformat(),
                    "card_count": len(daily_cards),
                    "decks": list(set(c.deck_name for c in daily_cards))
                })
            current_date = review_date
            daily_cards = []
        
        daily_cards.append(card)
    
    # Add the last group
    if current_date is not None:
        upcoming_reviews.append({
            "date": current_date.isoformat(),
            "card_count": len(daily_cards),
            "decks": list(set(c.deck_name for c in daily_cards))
        })
    
    return UpcomingReviewsResponse(
        period_days=days,
        upcoming_reviews=upcoming_reviews
    )
