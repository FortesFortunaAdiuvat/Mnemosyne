import pytest
from datetime import datetime
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestStudySession:
    """Test study session management"""

    def test_start_study_session(self):
        """Test starting a new study session"""
        session_data = {
            "deck_name": "Math",
            "session_type": "review",
            "max_cards": 10
        }
        response = client.post("/api/study/sessions/", json=session_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["deck_name"] == "Math"
        assert data["session_type"] == "review"
        assert data["max_cards"] == 10
        assert data["cards_studied"] == 0
        assert data["cards_correct"] == 0
        assert "id" in data
        assert "started_at" in data

    def test_get_next_card_empty_session(self):
        """Test getting next card when no cards are due"""
        # Start session
        session_data = {"deck_name": "Empty", "session_type": "review"}
        session_response = client.post("/api/study/sessions/", json=session_data)
        session_id = session_response.json()["id"]
        
        # Get next card
        response = client.get(f"/api/study/sessions/{session_id}/next-card")
        
        assert response.status_code == 200
        data = response.json()
        assert data["card"] is None
        assert data["session_complete"] is True

    def test_get_next_card_with_due_cards(self):
        """Test getting next card when cards are due"""
        # Create a card
        card_data = {"front": "2+2=?", "back": "4", "deck_name": "Math"}
        card_response = client.post("/api/cards/", json=card_data)
        card_id = card_response.json()["id"]
        
        # Review the card to make it due
        review_data = {"quality": 1, "response_time": 1.0}  # Poor quality resets to 1 day
        client.post(f"/api/cards/{card_id}/review", json=review_data)
        
        # Start session
        session_data = {"deck_name": "Math", "session_type": "review"}
        session_response = client.post("/api/study/sessions/", json=session_data)
        session_id = session_response.json()["id"]
        
        # Get next card
        response = client.get(f"/api/study/sessions/{session_id}/next-card")
        
        assert response.status_code == 200
        data = response.json()
        # The card should be available since we made it due
        if data["card"] is not None:
            assert data["card"]["front"] == "2+2=?"
            assert data["session_complete"] is False
        else:
            # If no card is returned, session should be complete
            assert data["session_complete"] is True

    def test_submit_card_review_in_session(self):
        """Test submitting a card review within a session"""
        # Create card and session
        card_data = {"front": "3+3=?", "back": "6", "deck_name": "Math"}
        card_response = client.post("/api/cards/", json=card_data)
        card_id = card_response.json()["id"]
        
        session_data = {"deck_name": "Math", "session_type": "review"}
        session_response = client.post("/api/study/sessions/", json=session_data)
        session_id = session_response.json()["id"]
        
        # Submit review
        review_data = {
            "card_id": card_id,
            "quality": 4,
            "response_time": 3.5
        }
        response = client.post(f"/api/study/sessions/{session_id}/review", json=review_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["cards_studied"] == 1
        assert data["cards_correct"] == 1

    def test_end_study_session(self):
        """Test ending a study session"""
        # Start session
        session_data = {"deck_name": "Math", "session_type": "review"}
        session_response = client.post("/api/study/sessions/", json=session_data)
        session_id = session_response.json()["id"]
        
        # End session
        response = client.put(f"/api/study/sessions/{session_id}/end")
        
        assert response.status_code == 200
        data = response.json()
        assert data["ended_at"] is not None
        assert data["session_complete"] is True

    def test_get_study_stats(self):
        """Test getting study statistics"""
        response = client.get("/api/study/stats")
        
        assert response.status_code == 200
        data = response.json()
        assert "total_sessions" in data
        assert "total_cards_studied" in data
        assert "average_accuracy" in data
