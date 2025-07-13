from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from app.core.database import get_db
from app.models.card import Card
from app.models.study_session import StudySession, CardReview
from app.models.schemas import (
    StudySessionCreate, StudySessionResponse, SessionReview, 
    NextCardResponse, StudyStatsResponse, CardResponse
)
from app.services.spaced_repetition import SM2Algorithm

router = APIRouter()


@router.post("/sessions/", response_model=StudySessionResponse, status_code=status.HTTP_201_CREATED)
def start_study_session(session_data: StudySessionCreate, db: Session = Depends(get_db)):
    """Start a new study session"""
    session = StudySession(**session_data.model_dump())
    db.add(session)
    db.commit()
    db.refresh(session)
    return StudySessionResponse(**session.__dict__, session_complete=False)


@router.get("/sessions/{session_id}/next-card", response_model=NextCardResponse)
def get_next_card(session_id: int, db: Session = Depends(get_db)):
    """Get the next card for review in the session"""
    session = db.query(StudySession).filter(StudySession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Get due cards for the session
    query = db.query(Card).filter(Card.next_review <= datetime.now())
    if session.deck_name:
        query = query.filter(Card.deck_name == session.deck_name)
    
    # Check if session is complete
    if session.cards_studied >= session.max_cards:
        return NextCardResponse(card=None, session_complete=True)
    
    card = query.order_by(Card.next_review).first()
    return NextCardResponse(
        card=CardResponse(**card.__dict__) if card else None,
        session_complete=card is None
    )


@router.post("/sessions/{session_id}/review", response_model=StudySessionResponse)
def submit_review(session_id: int, review: SessionReview, db: Session = Depends(get_db)):
    """Submit a card review within a session"""
    session = db.query(StudySession).filter(StudySession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    card = db.query(Card).filter(Card.id == review.card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    
    # Update card using SM-2 algorithm
    algorithm = SM2Algorithm()
    next_review_date, new_ease_factor, new_interval, new_repetitions = algorithm.calculate_next_review_date(
        quality=review.quality, ease_factor=card.ease_factor,
        interval=card.interval, repetitions=card.repetitions
    )
    
    card.ease_factor = new_ease_factor
    card.interval = new_interval
    card.repetitions = new_repetitions
    card.next_review = next_review_date
    card.last_reviewed = datetime.now()
    
    # Record the review
    card_review = CardReview(
        session_id=session_id, card_id=review.card_id,
        quality=review.quality, response_time=review.response_time
    )
    db.add(card_review)
    
    # Update session stats
    session.cards_studied += 1
    if review.quality >= 3:
        session.cards_correct += 1
    
    db.commit()
    db.refresh(session)
    return StudySessionResponse(**session.__dict__, session_complete=False)


@router.put("/sessions/{session_id}/end", response_model=StudySessionResponse)
def end_study_session(session_id: int, db: Session = Depends(get_db)):
    """End a study session"""
    session = db.query(StudySession).filter(StudySession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session.ended_at = datetime.now()
    db.commit()
    db.refresh(session)
    return StudySessionResponse(**session.__dict__, session_complete=True)


@router.get("/stats", response_model=StudyStatsResponse)
def get_study_stats(db: Session = Depends(get_db)):
    """Get overall study statistics"""
    total_sessions = db.query(StudySession).count()
    total_cards_studied = db.query(func.sum(StudySession.cards_studied)).scalar() or 0
    total_cards_correct = db.query(func.sum(StudySession.cards_correct)).scalar() or 0
    
    average_accuracy = (total_cards_correct / total_cards_studied * 100) if total_cards_studied > 0 else 0
    
    return StudyStatsResponse(
        total_sessions=total_sessions,
        total_cards_studied=total_cards_studied,
        average_accuracy=round(average_accuracy, 2)
    )
