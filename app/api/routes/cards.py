from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.card import Card
from app.models.schemas import CardCreate, CardResponse, CardUpdate, CardListResponse
from math import ceil

router = APIRouter()


@router.post("/", response_model=CardResponse, status_code=status.HTTP_201_CREATED)
def create_card(card: CardCreate, db: Session = Depends(get_db)):
    """Create a new card"""
    db_card = Card(
        front=card.front,
        back=card.back,
        deck_name=card.deck_name
    )
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card


@router.get("/", response_model=CardListResponse)
def get_cards(
    page: int = 1,
    size: int = 10,
    deck_name: str = None,
    db: Session = Depends(get_db)
):
    """Get all cards with pagination"""
    query = db.query(Card)
    
    if deck_name:
        query = query.filter(Card.deck_name == deck_name)
    
    total = query.count()
    cards = query.offset((page - 1) * size).limit(size).all()
    pages = ceil(total / size) if total > 0 else 0
    
    return CardListResponse(
        cards=cards,
        total=total,
        page=page,
        size=size,
        pages=pages
    )


@router.get("/{card_id}", response_model=CardResponse)
def get_card(card_id: int, db: Session = Depends(get_db)):
    """Get a specific card by ID"""
    card = db.query(Card).filter(Card.id == card_id).first()
    if card is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Card not found"
        )
    return card


@router.put("/{card_id}", response_model=CardResponse)
def update_card(card_id: int, card_update: CardUpdate, db: Session = Depends(get_db)):
    """Update a specific card"""
    card = db.query(Card).filter(Card.id == card_id).first()
    if card is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Card not found"
        )
    
    update_data = card_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(card, field, value)
    
    db.commit()
    db.refresh(card)
    return card


@router.delete("/{card_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_card(card_id: int, db: Session = Depends(get_db)):
    """Delete a specific card"""
    card = db.query(Card).filter(Card.id == card_id).first()
    if card is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Card not found"
        )
    
    db.delete(card)
    db.commit()
    return None
