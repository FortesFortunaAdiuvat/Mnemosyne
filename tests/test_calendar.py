import pytest
from datetime import datetime, date, timedelta
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import get_db
from app.models.card import Base

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_calendar.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_and_teardown():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


class TestCalendarIntegration:
    """Test calendar integration for learning habits and progress tracking"""

    def test_get_daily_due_count(self):
        """Test getting count of due cards for a specific date"""
        # Create some cards
        card1_data = {"front": "Q1", "back": "A1", "deck_name": "Math"}
        card2_data = {"front": "Q2", "back": "A2", "deck_name": "Science"}
        client.post("/api/cards/", json=card1_data)
        client.post("/api/cards/", json=card2_data)
        
        # Get due count for today
        today = date.today().isoformat()
        response = client.get(f"/api/calendar/due-count?date={today}")
        
        assert response.status_code == 200
        data = response.json()
        assert "date" in data
        assert "due_count" in data
        assert "by_deck" in data

    def test_get_weekly_progress(self):
        """Test getting weekly learning progress"""
        # Create a study session
        session_data = {"deck_name": "Math", "session_type": "review", "max_cards": 5}
        session_response = client.post("/api/study/sessions/", json=session_data)
        session_id = session_response.json()["id"]
        
        # End the session
        client.put(f"/api/study/sessions/{session_id}/end")
        
        # Get weekly progress
        today = date.today().isoformat()
        response = client.get(f"/api/calendar/weekly-progress?start_date={today}")
        
        assert response.status_code == 200
        data = response.json()
        assert "start_date" in data
        assert "end_date" in data
        assert "daily_stats" in data
        assert len(data["daily_stats"]) == 7

    def test_get_learning_streak(self):
        """Test getting current learning streak"""
        response = client.get("/api/calendar/streak")
        
        assert response.status_code == 200
        data = response.json()
        assert "current_streak" in data
        assert "longest_streak" in data
        assert "last_study_date" in data

    def test_get_monthly_heatmap(self):
        """Test getting monthly activity heatmap data"""
        # Get current month heatmap
        today = date.today()
        year_month = f"{today.year}-{today.month:02d}"
        response = client.get(f"/api/calendar/heatmap?year_month={year_month}")
        
        assert response.status_code == 200
        data = response.json()
        assert "year_month" in data
        assert "activity_data" in data
        assert isinstance(data["activity_data"], list)

    def test_get_deck_progress_over_time(self):
        """Test getting deck progress over time"""
        # Create cards in a specific deck
        card_data = {"front": "Test Q", "back": "Test A", "deck_name": "TestDeck"}
        client.post("/api/cards/", json=card_data)
        
        # Get deck progress
        response = client.get("/api/calendar/deck-progress?deck_name=TestDeck&days=30")
        
        assert response.status_code == 200
        data = response.json()
        assert "deck_name" in data
        assert "period_days" in data
        assert "progress_data" in data

    def test_schedule_daily_review_reminder(self):
        """Test scheduling daily review reminders"""
        reminder_data = {
            "time": "09:00",
            "enabled": True,
            "deck_names": ["Math", "Science"]
        }
        response = client.post("/api/calendar/reminder", json=reminder_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["time"] == "09:00"
        assert data["enabled"] is True
        assert "Math" in data["deck_names"]

    def test_get_upcoming_reviews(self):
        """Test getting upcoming review schedule"""
        # Create a card and review it to set future review date
        card_data = {"front": "Future Q", "back": "Future A", "deck_name": "Future"}
        card_response = client.post("/api/cards/", json=card_data)
        card_id = card_response.json()["id"]
        
        # Review the card to set next review date
        review_data = {"quality": 4, "response_time": 2.0}
        client.post(f"/api/cards/{card_id}/review", json=review_data)
        
        # Get upcoming reviews for next 7 days
        response = client.get("/api/calendar/upcoming?days=7")
        
        assert response.status_code == 200
        data = response.json()
        assert "period_days" in data
        assert "upcoming_reviews" in data
        assert isinstance(data["upcoming_reviews"], list)
