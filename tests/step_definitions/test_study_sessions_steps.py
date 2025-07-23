import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from fastapi.testclient import TestClient
from app.main import app
import time

# Load scenarios from the feature file
scenarios('../features/study_sessions.feature')

# Test client fixture
@pytest.fixture
def client():
    return TestClient(app)

# Context to store test data
@pytest.fixture
def context():
    return {}


# Background steps
@given("the Mnemosyne learning system is running")
def mnemosyne_system_running(client):
    """Verify the system is running by checking health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200


@given("I have access to the study session API")
def study_session_api_access(client):
    """Verify study session API is accessible"""
    response = client.get("/api/study/stats")
    assert response.status_code == 200


# Scenario: Starting a new study session
@given(parsers.parse('I want to study my "{deck_name}" flashcards'))
def want_to_study_deck(context, deck_name):
    """Set the deck name for studying"""
    context['study_deck'] = deck_name


@when(parsers.parse('I start a study session for the "{deck_name}" deck with a maximum of {max_cards:d} cards'))
def start_study_session(context, client, deck_name, max_cards):
    """Start a new study session"""
    session_data = {
        "deck_name": deck_name,
        "session_type": "review",
        "max_cards": max_cards
    }
    response = client.post("/api/study/sessions/", json=session_data)
    context['session_response'] = response
    if response.status_code == 201:
        context['active_session'] = response.json()


@then("a new study session should be created")
def study_session_should_be_created(context):
    """Verify a new study session was created"""
    assert context['session_response'].status_code == 201
    assert 'active_session' in context
    assert 'id' in context['active_session']


@then(parsers.parse('the session should be configured for the "{deck_name}" deck'))
def session_configured_for_deck(context, deck_name):
    """Verify the session is configured for the correct deck"""
    assert context['active_session']['deck_name'] == deck_name


@then(parsers.parse('the session should be limited to {max_cards:d} cards maximum'))
def session_limited_to_max_cards(context, max_cards):
    """Verify the session has the correct card limit"""
    assert context['active_session']['max_cards'] == max_cards


@then(parsers.parse('the session should show {cards_studied:d} cards studied initially'))
def session_shows_initial_cards_studied(context, cards_studied):
    """Verify the session shows correct initial cards studied count"""
    assert context['active_session']['cards_studied'] == cards_studied


# Scenario: Getting the next card in an active session
@given(parsers.parse('I have an active study session for "{deck_name}" deck'))
def have_active_study_session(context, client, deck_name):
    """Create an active study session"""
    session_data = {
        "deck_name": deck_name,
        "session_type": "review",
        "max_cards": 10
    }
    response = client.post("/api/study/sessions/", json=session_data)
    assert response.status_code == 201
    context['active_session'] = response.json()


@given(parsers.parse('there are flashcards due for review in the "{deck_name}" deck'))
def have_flashcards_due_in_deck(context, client, deck_name):
    """Create flashcards that are due for review in the specified deck"""
    cards_data = [
        {"front": "Science Q1", "back": "Science A1", "deck_name": deck_name},
        {"front": "Science Q2", "back": "Science A2", "deck_name": deck_name},
    ]
    
    context['deck_cards'] = []
    for card_data in cards_data:
        response = client.post("/api/cards/", json=card_data)
        assert response.status_code == 201
        context['deck_cards'].append(response.json())
    
    # Wait to ensure cards are due
    time.sleep(1)


@when("I request the next card to review")
def request_next_card(context, client):
    """Request the next card in the study session"""
    session_id = context['active_session']['id']
    response = client.get(f"/api/study/sessions/{session_id}/next-card")
    context['next_card_response'] = response
    if response.status_code == 200:
        context['next_card_data'] = response.json()


@then(parsers.parse('I should receive a flashcard from the "{deck_name}" deck'))
def should_receive_flashcard_from_deck(context, deck_name):
    """Verify a flashcard from the correct deck is received"""
    assert context['next_card_response'].status_code == 200
    next_card_data = context['next_card_data']
    if next_card_data['card'] is not None:
        assert next_card_data['card']['deck_name'] == deck_name


@then("the session should not be marked as complete")
def session_should_not_be_complete(context):
    """Verify the session is not marked as complete"""
    next_card_data = context['next_card_data']
    assert next_card_data['session_complete'] is False


@then("the flashcard should be ready for review")
def flashcard_should_be_ready_for_review(context):
    """Verify the flashcard is ready for review"""
    next_card_data = context['next_card_data']
    if next_card_data['card'] is not None:
        card = next_card_data['card']
        assert 'front' in card
        assert 'back' in card
        assert 'id' in card


# Scenario: Getting next card when no cards are due
@given(parsers.parse('there are no flashcards due for review in the "{deck_name}" deck'))
def no_flashcards_due_in_deck(context, deck_name):
    """Ensure no flashcards are due for review in the specified deck"""
    # Don't create any cards, or create cards that are not due
    context['no_due_cards'] = True


@then("I should receive no flashcard")
def should_receive_no_flashcard(context):
    """Verify no flashcard is received"""
    assert context['next_card_response'].status_code == 200
    next_card_data = context['next_card_data']
    assert next_card_data['card'] is None


@then("the session should be marked as complete")
def session_should_be_marked_complete(context):
    """Verify the session is marked as complete"""
    next_card_data = context['next_card_data']
    assert next_card_data['session_complete'] is True


@then("I should be notified that no more cards are available")
def should_be_notified_no_cards_available(context):
    """Verify notification that no cards are available"""
    next_card_data = context['next_card_data']
    assert next_card_data['card'] is None
    assert next_card_data['session_complete'] is True


# Scenario: Reviewing a card within a study session
@given("I have an active study session")
def have_active_study_session_generic(context, client):
    """Create a generic active study session"""
    session_data = {
        "deck_name": "Test",
        "session_type": "review",
        "max_cards": 10
    }
    response = client.post("/api/study/sessions/", json=session_data)
    assert response.status_code == 201
    context['active_session'] = response.json()


@given("I have received a flashcard to review")
def have_received_flashcard_to_review(context, client):
    """Create a flashcard and simulate receiving it for review"""
    card_data = {
        "front": "Test question for session",
        "back": "Test answer for session",
        "deck_name": "Test"
    }
    response = client.post("/api/cards/", json=card_data)
    assert response.status_code == 201
    context['session_card'] = response.json()


@when(parsers.parse('I submit my review with quality score {quality:d} and response time {response_time:f} seconds'))
def submit_review_in_session(context, client, quality, response_time):
    """Submit a review within the study session"""
    session_id = context['active_session']['id']
    card_id = context['session_card']['id']
    
    review_data = {
        "card_id": card_id,
        "quality": quality,
        "response_time": response_time
    }
    response = client.post(f"/api/study/sessions/{session_id}/review", json=review_data)
    context['session_review_response'] = response
    context['review_quality'] = quality
    if response.status_code == 200:
        context['updated_session'] = response.json()


@then(parsers.parse("the session's cards studied count should increase by {increment:d}"))
def session_cards_studied_should_increase(context, increment):
    """Verify the session's cards studied count increased"""
    assert context['session_review_response'].status_code == 200
    original_count = context['active_session']['cards_studied']
    new_count = context['updated_session']['cards_studied']
    assert new_count == original_count + increment


@then(parsers.parse("the session's correct answers count should increase by {increment:d}"))
def session_correct_answers_should_increase(context, increment):
    """Verify the session's correct answers count increased"""
    original_count = context['active_session']['cards_correct']
    new_count = context['updated_session']['cards_correct']
    if context['review_quality'] >= 3:  # Good performance
        assert new_count == original_count + increment


@then("the session's correct answers count should remain unchanged")
def session_correct_answers_should_remain_unchanged(context):
    """Verify the session's correct answers count remained unchanged"""
    original_count = context['active_session']['cards_correct']
    new_count = context['updated_session']['cards_correct']
    if context['review_quality'] < 3:  # Poor performance
        assert new_count == original_count


@then("the flashcard should be updated with the new review data")
def flashcard_should_be_updated_with_review_data(context, client):
    """Verify the flashcard was updated with review data"""
    card_id = context['session_card']['id']
    response = client.get(f"/api/cards/{card_id}")
    assert response.status_code == 200
    updated_card = response.json()
    
    # Card should have been reviewed (last_reviewed should be set)
    assert updated_card['last_reviewed'] is not None
    # Repetitions should have changed based on quality
    if context['review_quality'] >= 3:
        assert updated_card['repetitions'] > context['session_card']['repetitions']
    else:
        assert updated_card['repetitions'] == 0  # Reset for poor performance


@then("the flashcard should be rescheduled appropriately")
def flashcard_should_be_rescheduled_appropriately_in_session(context, client):
    """Verify the flashcard was rescheduled appropriately"""
    card_id = context['session_card']['id']
    response = client.get(f"/api/cards/{card_id}")
    assert response.status_code == 200
    updated_card = response.json()
    
    # Next review should be set
    assert updated_card['next_review'] is not None
    # Interval should be appropriate for the quality
    if context['review_quality'] < 3:
        assert updated_card['interval'] == 1  # Reset to 1 day for poor performance


# Scenario: Ending a study session
@when("I end the study session")
def end_study_session(context, client):
    """End the active study session"""
    session_id = context['active_session']['id']
    response = client.put(f"/api/study/sessions/{session_id}/end")
    context['end_session_response'] = response
    if response.status_code == 200:
        context['ended_session'] = response.json()


@then("the session should have an end timestamp")
def session_should_have_end_timestamp(context):
    """Verify the session has an end timestamp"""
    assert context['end_session_response'].status_code == 200
    assert context['ended_session']['ended_at'] is not None


@then("I should be able to see my session results")
def should_see_session_results(context):
    """Verify session results are available"""
    ended_session = context['ended_session']
    assert 'cards_studied' in ended_session
    assert 'cards_correct' in ended_session
    assert 'started_at' in ended_session
    assert 'ended_at' in ended_session


# Scenario: Reaching the maximum card limit in a session
@given(parsers.parse('I have a study session limited to {max_cards:d} cards'))
def have_session_limited_to_cards(context, client, max_cards):
    """Create a study session with a specific card limit"""
    session_data = {
        "deck_name": "Limited",
        "session_type": "review",
        "max_cards": max_cards
    }
    response = client.post("/api/study/sessions/", json=session_data)
    assert response.status_code == 201
    context['limited_session'] = response.json()
    context['max_cards'] = max_cards


@given(parsers.parse('I have already studied {cards_studied:d} cards in this session'))
def have_already_studied_cards(context, client, cards_studied):
    """Simulate having already studied the specified number of cards"""
    session_id = context['limited_session']['id']
    
    # Create cards and review them to reach the limit
    for i in range(cards_studied):
        # Create a card
        card_data = {
            "front": f"Question {i+1}",
            "back": f"Answer {i+1}",
            "deck_name": "Limited"
        }
        card_response = client.post("/api/cards/", json=card_data)
        assert card_response.status_code == 201
        card = card_response.json()
        
        # Review the card in the session
        review_data = {
            "card_id": card['id'],
            "quality": 4,
            "response_time": 2.0
        }
        review_response = client.post(f"/api/study/sessions/{session_id}/review", json=review_data)
        assert review_response.status_code == 200
        context['limited_session'] = review_response.json()


@then("I should be notified that the session limit has been reached")
def should_be_notified_session_limit_reached(context):
    """Verify notification that session limit has been reached"""
    next_card_data = context['next_card_data']
    assert next_card_data['card'] is None
    assert next_card_data['session_complete'] is True
    
    # Verify the session has reached its limit
    assert context['limited_session']['cards_studied'] >= context['max_cards']


# Scenario: Viewing my overall study statistics
@given("I have completed several study sessions")
def have_completed_several_sessions(context, client):
    """Create and complete several study sessions"""
    context['completed_sessions'] = []
    
    for i in range(3):
        # Start session
        session_data = {
            "deck_name": f"Stats{i}",
            "session_type": "review",
            "max_cards": 5
        }
        session_response = client.post("/api/study/sessions/", json=session_data)
        assert session_response.status_code == 201
        session = session_response.json()
        
        # Create and review some cards
        for j in range(2):
            card_data = {
                "front": f"Stats Q{i}-{j}",
                "back": f"Stats A{i}-{j}",
                "deck_name": f"Stats{i}"
            }
            card_response = client.post("/api/cards/", json=card_data)
            assert card_response.status_code == 201
            card = card_response.json()
            
            review_data = {
                "card_id": card['id'],
                "quality": 4,
                "response_time": 3.0
            }
            client.post(f"/api/study/sessions/{session['id']}/review", json=review_data)
        
        # End session
        end_response = client.put(f"/api/study/sessions/{session['id']}/end")
        assert end_response.status_code == 200
        context['completed_sessions'].append(end_response.json())


@when("I request my overall study statistics")
def request_overall_study_statistics(context, client):
    """Request overall study statistics"""
    response = client.get("/api/study/stats")
    context['stats_response'] = response
    if response.status_code == 200:
        context['study_stats'] = response.json()


@then("I should see the total number of study sessions completed")
def should_see_total_sessions_completed(context):
    """Verify total sessions count is shown"""
    assert context['stats_response'].status_code == 200
    stats = context['study_stats']
    assert 'total_sessions' in stats
    assert stats['total_sessions'] >= len(context['completed_sessions'])


@then("I should see the total number of cards I have studied")
def should_see_total_cards_studied(context):
    """Verify total cards studied count is shown"""
    stats = context['study_stats']
    assert 'total_cards_studied' in stats
    assert stats['total_cards_studied'] >= 0


@then("I should see my average accuracy percentage across all sessions")
def should_see_average_accuracy_percentage(context):
    """Verify average accuracy percentage is shown"""
    stats = context['study_stats']
    assert 'average_accuracy' in stats
    assert 0 <= stats['average_accuracy'] <= 100


# Error scenarios
@given("I try to get the next card from a session that doesn't exist")
def try_get_next_card_nonexistent_session(context):
    """Prepare to get next card from non-existent session"""
    context['nonexistent_session_id'] = 99999


@when("I submit the request")
def submit_next_card_request(context, client):
    """Submit request for next card from non-existent session"""
    session_id = context['nonexistent_session_id']
    response = client.get(f"/api/study/sessions/{session_id}/next-card")
    context['nonexistent_next_card_response'] = response


@then("I should receive an error message")
def should_receive_error_message_for_session(context):
    """Verify error message for non-existent session"""
    assert context['nonexistent_next_card_response'].status_code == 404


@then("the system should indicate the session was not found")
def system_indicates_session_not_found(context):
    """Verify the error indicates session not found"""
    response_data = context['nonexistent_next_card_response'].json()
    assert "not found" in response_data['detail'].lower()


@given("I try to submit a review to a session that doesn't exist")
def try_submit_review_nonexistent_session(context):
    """Prepare to submit review to non-existent session"""
    context['nonexistent_session_id'] = 99999


@when("I submit the review request")
def submit_review_request_nonexistent_session(context, client):
    """Submit review request to non-existent session"""
    session_id = context['nonexistent_session_id']
    review_data = {
        "card_id": 1,
        "quality": 4,
        "response_time": 3.0
    }
    response = client.post(f"/api/study/sessions/{session_id}/review", json=review_data)
    context['nonexistent_review_response'] = response


@then("I should receive an error message")
def should_receive_error_message_for_review_session(context):
    """Verify error message for review to non-existent session"""
    assert context['nonexistent_review_response'].status_code == 404
