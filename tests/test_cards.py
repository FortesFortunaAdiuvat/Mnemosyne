import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestCardCreation:
    """Test card creation functionality"""

    def test_create_card_success(self):
        """Test creating a card successfully"""
        card_data = {
            "front": "What is the capital of France?",
            "back": "Paris",
            "deck_name": "Geography"
        }
        
        response = client.post("/api/cards", json=card_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["front"] == card_data["front"]
        assert data["back"] == card_data["back"]
        assert data["deck_name"] == card_data["deck_name"]
        assert "id" in data
        assert data["ease_factor"] == 2.5
        assert data["interval"] == 1
        assert data["repetitions"] == 0
        assert "created_at" in data
        assert "next_review" in data

    def test_create_card_minimal_data(self):
        """Test creating a card with minimal required data"""
        card_data = {
            "front": "Question",
            "back": "Answer"
        }
        
        response = client.post("/api/cards", json=card_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["front"] == card_data["front"]
        assert data["back"] == card_data["back"]
        assert data["deck_name"] == "default"  # Should use default deck

    def test_create_card_missing_front(self):
        """Test creating a card without front field"""
        card_data = {
            "back": "Answer"
        }
        
        response = client.post("/api/cards", json=card_data)
        
        assert response.status_code == 422  # Validation error

    def test_create_card_missing_back(self):
        """Test creating a card without back field"""
        card_data = {
            "front": "Question"
        }
        
        response = client.post("/api/cards", json=card_data)
        
        assert response.status_code == 422  # Validation error

    def test_create_card_empty_front(self):
        """Test creating a card with empty front field"""
        card_data = {
            "front": "",
            "back": "Answer"
        }
        
        response = client.post("/api/cards", json=card_data)
        
        assert response.status_code == 422  # Validation error

    def test_create_card_empty_back(self):
        """Test creating a card with empty back field"""
        card_data = {
            "front": "Question",
            "back": ""
        }
        
        response = client.post("/api/cards", json=card_data)
        
        assert response.status_code == 422  # Validation error


class TestCardRetrieval:
    """Test card retrieval functionality"""

    def test_get_cards_empty_list(self):
        """Test getting cards when none exist"""
        response = client.get("/api/cards")
        
        assert response.status_code == 200
        data = response.json()
        assert data["cards"] == []
        assert data["total"] == 0
        assert data["page"] == 1
        assert data["size"] == 10
        assert data["pages"] == 0

    def test_get_card_by_id_not_found(self):
        """Test getting a card that doesn't exist"""
        response = client.get("/api/cards/999")
        
        assert response.status_code == 404

    def test_get_cards_with_data(self):
        """Test getting cards when some exist"""
        # Create a card first
        card_data = {
            "front": "Test Question",
            "back": "Test Answer",
            "deck_name": "Test Deck"
        }
        client.post("/api/cards", json=card_data)
        
        response = client.get("/api/cards")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["cards"]) == 1
        assert data["total"] == 1
        assert data["cards"][0]["front"] == card_data["front"]

    def test_get_card_by_id_success(self):
        """Test getting a card that exists"""
        # Create a card first
        card_data = {
            "front": "Test Question",
            "back": "Test Answer"
        }
        create_response = client.post("/api/cards", json=card_data)
        card_id = create_response.json()["id"]
        
        response = client.get(f"/api/cards/{card_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["front"] == card_data["front"]
        assert data["back"] == card_data["back"]
        assert data["id"] == card_id


class TestCardUpdate:
    """Test card update functionality"""

    def test_update_card_success(self):
        """Test updating a card successfully"""
        # Create a card first
        card_data = {
            "front": "Original Question",
            "back": "Original Answer"
        }
        create_response = client.post("/api/cards", json=card_data)
        card_id = create_response.json()["id"]
        
        # Update the card
        update_data = {
            "front": "Updated Question",
            "back": "Updated Answer"
        }
        response = client.put(f"/api/cards/{card_id}", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["front"] == update_data["front"]
        assert data["back"] == update_data["back"]
        assert data["id"] == card_id

    def test_update_card_partial(self):
        """Test updating only some fields of a card"""
        # Create a card first
        card_data = {
            "front": "Original Question",
            "back": "Original Answer",
            "deck_name": "Original Deck"
        }
        create_response = client.post("/api/cards", json=card_data)
        card_id = create_response.json()["id"]
        
        # Update only the front
        update_data = {"front": "Updated Question"}
        response = client.put(f"/api/cards/{card_id}", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["front"] == update_data["front"]
        assert data["back"] == card_data["back"]  # Should remain unchanged
        assert data["deck_name"] == card_data["deck_name"]  # Should remain unchanged

    def test_update_card_not_found(self):
        """Test updating a card that doesn't exist"""
        update_data = {"front": "Updated Question"}
        response = client.put("/api/cards/999", json=update_data)
        
        assert response.status_code == 404


class TestCardDeletion:
    """Test card deletion functionality"""

    def test_delete_card_success(self):
        """Test deleting a card successfully"""
        # Create a card first
        card_data = {
            "front": "To be deleted",
            "back": "Delete me"
        }
        create_response = client.post("/api/cards", json=card_data)
        card_id = create_response.json()["id"]
        
        # Delete the card
        response = client.delete(f"/api/cards/{card_id}")
        
        assert response.status_code == 204
        
        # Verify it's deleted
        get_response = client.get(f"/api/cards/{card_id}")
        assert get_response.status_code == 404

    def test_delete_card_not_found(self):
        """Test deleting a card that doesn't exist"""
        response = client.delete("/api/cards/999")
        
        assert response.status_code == 404
