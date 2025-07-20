import pytest
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from app.main import app
from app.services.spaced_repetition import SM2Algorithm

client = TestClient(app)


class TestSM2Algorithm:
    """Test SM-2 spaced repetition algorithm"""

    def test_sm2_first_correct_review(self):
        """Test first correct review (quality >= 3)"""
        algorithm = SM2Algorithm()
        
        # Initial state: new card
        ease_factor = 2.5
        interval = 1
        repetitions = 0
        quality = 5  # Perfect response (should increase ease factor)
        
        new_interval, new_ease_factor, new_repetitions = algorithm.calculate_next_review(
            quality, ease_factor, interval, repetitions
        )
        
        assert new_interval == 1  # First correct review stays at 1 day
        assert new_repetitions == 1
        assert new_ease_factor > ease_factor  # Should increase for quality 5

    def test_sm2_second_correct_review(self):
        """Test second correct review"""
        algorithm = SM2Algorithm()
        
        # After first correct review
        ease_factor = 2.6
        interval = 1
        repetitions = 1
        quality = 5  # Perfect response
        
        new_interval, new_ease_factor, new_repetitions = algorithm.calculate_next_review(
            quality, ease_factor, interval, repetitions
        )
        
        assert new_interval == 6  # Second correct review goes to 6 days
        assert new_repetitions == 2
        assert new_ease_factor > ease_factor

    def test_sm2_third_correct_review(self):
        """Test third and subsequent correct reviews"""
        algorithm = SM2Algorithm()
        
        # After second correct review
        ease_factor = 2.7
        interval = 6
        repetitions = 2
        quality = 5  # Perfect response
        
        new_interval, new_ease_factor, new_repetitions = algorithm.calculate_next_review(
            quality, ease_factor, interval, repetitions
        )
        
        expected_interval = round(6 * 2.7)  # interval * ease_factor
        assert new_interval == expected_interval
        assert new_repetitions == 3
        assert new_ease_factor > ease_factor

    def test_sm2_incorrect_review(self):
        """Test incorrect review (quality < 3)"""
        algorithm = SM2Algorithm()
        
        # Card with some progress
        ease_factor = 2.5
        interval = 15
        repetitions = 3
        quality = 1  # Poor response
        
        new_interval, new_ease_factor, new_repetitions = algorithm.calculate_next_review(
            quality, ease_factor, interval, repetitions
        )
        
        assert new_interval == 1  # Reset to 1 day
        assert new_repetitions == 0  # Reset repetitions
        assert new_ease_factor < ease_factor  # Should decrease for poor quality

    def test_sm2_ease_factor_minimum(self):
        """Test that ease factor doesn't go below minimum"""
        algorithm = SM2Algorithm()
        
        ease_factor = 1.3  # At minimum
        interval = 1
        repetitions = 0
        quality = 0  # Worst possible response
        
        new_interval, new_ease_factor, new_repetitions = algorithm.calculate_next_review(
            quality, ease_factor, interval, repetitions
        )
        
        assert new_ease_factor >= 1.3  # Should not go below minimum

    def test_sm2_perfect_response(self):
        """Test perfect response (quality = 5)"""
        algorithm = SM2Algorithm()
        
        ease_factor = 2.5
        interval = 1
        repetitions = 0
        quality = 5  # Perfect response
        
        new_interval, new_ease_factor, new_repetitions = algorithm.calculate_next_review(
            quality, ease_factor, interval, repetitions
        )
        
        assert new_repetitions == 1
        assert new_ease_factor > ease_factor  # Should increase significantly


class TestCardReviewAPI:
    """Test card review API endpoints"""

    def test_review_card_success(self):
        """Test reviewing a card successfully"""
        # Create a card first
        card_data = {
            "front": "What is 2+2?",
            "back": "4",
            "deck_name": "Math"
        }
        create_response = client.post("/api/cards/", json=card_data)
        card_id = create_response.json()["id"]
        
        # Review the card
        review_data = {
            "quality": 4,
            "response_time": 3.5
        }
        response = client.post(f"/api/cards/{card_id}/review", json=review_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == card_id
        assert data["repetitions"] == 1  # Should increment
        assert data["last_reviewed"] is not None
        assert data["next_review"] is not None

    def test_review_card_incorrect(self):
        """Test reviewing a card incorrectly"""
        # Create a card first
        card_data = {
            "front": "What is the capital of Mars?",
            "back": "There is no capital of Mars",
            "deck_name": "Astronomy"
        }
        create_response = client.post("/api/cards/", json=card_data)
        card_id = create_response.json()["id"]
        
        # Review the card incorrectly
        review_data = {
            "quality": 1,
            "response_time": 10.0
        }
        response = client.post(f"/api/cards/{card_id}/review", json=review_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["repetitions"] == 0  # Should reset to 0
        assert data["interval"] == 1  # Should reset to 1 day

    def test_review_card_not_found(self):
        """Test reviewing a card that doesn't exist"""
        review_data = {
            "quality": 4,
            "response_time": 3.5
        }
        response = client.post("/api/cards/999/review", json=review_data)
        
        assert response.status_code == 404

    def test_review_card_invalid_quality(self):
        """Test reviewing a card with invalid quality score"""
        # Create a card first
        card_data = {
            "front": "Test question",
            "back": "Test answer"
        }
        create_response = client.post("/api/cards/", json=card_data)
        card_id = create_response.json()["id"]
        
        # Review with invalid quality
        review_data = {
            "quality": 6,  # Invalid: should be 0-5
            "response_time": 3.5
        }
        response = client.post(f"/api/cards/{card_id}/review", json=review_data)
        
        assert response.status_code == 422  # Validation error


class TestDueCards:
    """Test due cards functionality"""

    def test_get_due_cards_empty(self):
        """Test getting due cards when none are due"""
        response = client.get("/api/cards/due")
        
        assert response.status_code == 200
        data = response.json()
        assert data["cards"] == []
        assert data["total"] == 0

    def test_get_due_cards_with_data(self):
        """Test getting due cards when some are due"""
        # Create a card - it should be due immediately upon creation
        card_data = {
            "front": "Due card",
            "back": "Answer"
        }
        create_response = client.post("/api/cards/", json=card_data)
        
        # Wait to ensure card is definitely due
        import time
        time.sleep(1)
        
        # New cards should be due immediately (next_review defaults to now)
        response = client.get("/api/cards/due")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["cards"]) >= 1
        assert data["total"] >= 1
        assert data["cards"][0]["front"] == "Due card"

    def test_get_due_cards_by_deck(self):
        """Test getting due cards filtered by deck"""
        # Create cards in different decks - they should be due immediately
        card1_data = {"front": "Q1", "back": "A1", "deck_name": "Deck1"}
        card2_data = {"front": "Q2", "back": "A2", "deck_name": "Deck2"}
        
        client.post("/api/cards/", json=card1_data)
        client.post("/api/cards/", json=card2_data)
        
        # Wait to ensure cards are definitely due
        import time
        time.sleep(1)
        
        # Get due cards for specific deck
        response = client.get("/api/cards/due?deck_name=Deck1")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["cards"]) >= 1
        # Verify the returned card is from Deck1
        assert data["cards"][0]["deck_name"] == "Deck1"
        assert data["cards"][0]["front"] == "Q1"
