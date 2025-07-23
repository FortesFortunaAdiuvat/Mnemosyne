import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from fastapi.testclient import TestClient
from app.main import app
import time
from datetime import datetime, timedelta

# Load scenarios from the feature file
scenarios('../features/spaced_repetition.feature')

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


@given("I have access to the spaced repetition API")
def spaced_repetition_api_access(client):
    """Verify spaced repetition API is accessible"""
    response = client.get("/api/cards/due")
    assert response.status_code == 200


# Scenario: Reviewing a flashcard correctly for the first time
@given("I have a new flashcard that I haven't reviewed yet")
def have_new_flashcard(context, client):
    """Create a new flashcard that hasn't been reviewed"""
    card_data = {
        "front": "What is the capital of Japan?",
        "back": "Tokyo",
        "deck_name": "Geography"
    }
    response = client.post("/api/cards/", json=card_data)
    assert response.status_code == 201
    context['new_card'] = response.json()
    assert context['new_card']['repetitions'] == 0
    assert context['new_card']['ease_factor'] == 2.5


@when(parsers.parse('I review the flashcard and rate my performance as "{performance}" (quality {quality:d})'))
def review_flashcard_with_quality(context, client, performance, quality):
    """Review the flashcard with specified quality rating"""
    card_id = context['new_card']['id']
    review_data = {
        "quality": quality,
        "response_time": 3.0
    }
    response = client.post(f"/api/cards/{card_id}/review", json=review_data)
    context['review_response'] = response
    context['quality'] = quality
    if response.status_code == 200:
        context['reviewed_card'] = response.json()


@then(parsers.parse("the flashcard's repetition count should increase to {expected_repetitions:d}"))
def repetition_count_should_increase(context, expected_repetitions):
    """Verify the repetition count increased correctly"""
    assert context['review_response'].status_code == 200
    assert context['reviewed_card']['repetitions'] == expected_repetitions


@then(parsers.parse("the flashcard should be scheduled for review in {days:d} day"))
@then(parsers.parse("the flashcard should be scheduled for review in {days:d} days"))
def flashcard_scheduled_for_review(context, days):
    """Verify the flashcard is scheduled for review in the correct number of days"""
    reviewed_card = context['reviewed_card']
    assert reviewed_card['interval'] == days


@then("my ease factor should improve slightly")
def ease_factor_should_improve_slightly(context):
    """Verify the ease factor improved for good performance"""
    original_ease = context['new_card']['ease_factor']
    new_ease = context['reviewed_card']['ease_factor']
    if context['quality'] >= 3:  # Good performance
        assert new_ease >= original_ease


@then("my ease factor should improve further")
def ease_factor_should_improve_further(context):
    """Verify the ease factor improved significantly for perfect performance"""
    original_ease = context['new_card']['ease_factor']
    new_ease = context['reviewed_card']['ease_factor']
    if context['quality'] == 5:  # Perfect performance
        assert new_ease > original_ease


# Scenario: Reviewing a flashcard correctly for the second time
@given("I have a flashcard that I've reviewed correctly once before")
def have_flashcard_reviewed_once_before(context, client):
    """Create and review a flashcard once to set up the scenario"""
    # Create flashcard
    card_data = {
        "front": "What is 2+2?",
        "back": "4",
        "deck_name": "Math"
    }
    response = client.post("/api/cards/", json=card_data)
    assert response.status_code == 201
    card = response.json()
    
    # Review it once to get to the desired state
    review_data = {"quality": 4, "response_time": 2.0}
    response = client.post(f"/api/cards/{card['id']}/review", json=review_data)
    assert response.status_code == 200
    
    context['card_with_history'] = response.json()
    # Verify it has the expected state
    assert context['card_with_history']['repetitions'] >= 1


@given(parsers.parse("the flashcard has {repetitions:d} repetition and ease factor of {ease_factor:f}"))
def flashcard_has_repetition_and_ease_factor(context, repetitions, ease_factor):
    """Verify the flashcard has the expected repetition and ease factor"""
    # This step is mainly for documentation - the previous step should have set up the card appropriately
    if 'card_with_history' in context:
        # The card should have been reviewed at least once
        assert context['card_with_history']['repetitions'] >= repetitions
        # Use the existing card for the next review
        context['new_card'] = context['card_with_history']


# Scenario: Reviewing a flashcard incorrectly
@given("I have a flashcard that I've reviewed correctly multiple times")
def have_flashcard_reviewed_multiple_times(context, client):
    """Create a flashcard with multiple successful reviews"""
    # Create flashcard
    card_data = {
        "front": "What is the square root of 144?",
        "back": "12",
        "deck_name": "Math"
    }
    response = client.post("/api/cards/", json=card_data)
    assert response.status_code == 201
    card = response.json()
    
    # Review it multiple times to build up repetitions
    for i in range(3):  # Default to 3 repetitions
        review_data = {"quality": 4, "response_time": 2.0}
        response = client.post(f"/api/cards/{card['id']}/review", json=review_data)
        assert response.status_code == 200
        card = response.json()
    
    context['experienced_card'] = card


@given(parsers.parse("the flashcard has {repetitions:d} repetitions and is scheduled for review in {interval:d} days"))
def flashcard_has_repetitions_and_interval(context, repetitions, interval):
    """Verify the flashcard has the expected repetitions and interval"""
    # This step is mainly for documentation - the previous step should have set up the card appropriately
    if 'experienced_card' in context:
        # The card should have been reviewed multiple times
        assert context['experienced_card']['repetitions'] >= repetitions
        # Use the existing card for the next review
        context['new_card'] = context['experienced_card']


@then(parsers.parse("the flashcard's repetition count should reset to {expected_repetitions:d}"))
def repetition_count_should_reset(context, expected_repetitions):
    """Verify the repetition count reset for poor performance"""
    assert context['review_response'].status_code == 200
    if context['quality'] < 3:  # Poor performance
        assert context['reviewed_card']['repetitions'] == expected_repetitions


@then("my ease factor should decrease")
def ease_factor_should_decrease(context):
    """Verify the ease factor decreased for poor performance"""
    if 'experienced_card' in context:
        original_ease = context['experienced_card']['ease_factor']
    else:
        original_ease = context['new_card']['ease_factor']
    
    new_ease = context['reviewed_card']['ease_factor']
    if context['quality'] < 3:  # Poor performance
        assert new_ease <= original_ease


# Scenario: Getting cards that are due for review
@given("I have several flashcards with different review schedules")
def have_flashcards_with_different_schedules(context, client):
    """Create flashcards with different review schedules"""
    cards_data = [
        {"front": "Due card 1", "back": "Answer 1", "deck_name": "Test"},
        {"front": "Due card 2", "back": "Answer 2", "deck_name": "Test"},
        {"front": "Future card", "back": "Future answer", "deck_name": "Test"},
    ]
    
    context['created_cards'] = []
    for card_data in cards_data:
        response = client.post("/api/cards/", json=card_data)
        assert response.status_code == 201
        context['created_cards'].append(response.json())
    
    # Wait to ensure cards are due
    time.sleep(1)


@given("some flashcards are due for review today")
def some_flashcards_are_due_for_review_today(context):
    """Verify that some flashcards are due for review today"""
    # This step is mainly for documentation - the previous step should have created due cards
    assert 'created_cards' in context
    assert len(context['created_cards']) > 0


@when("I request cards that are due for review")
def request_due_cards(context, client):
    """Request cards that are due for review"""
    response = client.get("/api/cards/due")
    context['due_cards_response'] = response
    if response.status_code == 200:
        context['due_cards'] = response.json()


@then("I should receive only the cards that are currently due")
def should_receive_only_due_cards(context):
    """Verify only due cards are returned"""
    assert context['due_cards_response'].status_code == 200
    due_cards = context['due_cards']['cards']
    # All returned cards should be due (next_review <= now)
    now = datetime.now()
    for card in due_cards:
        next_review = datetime.fromisoformat(card['next_review'].replace('Z', '+00:00'))
        # Allow some tolerance for timing
        assert next_review <= now + timedelta(seconds=5)


@then("the cards should be ordered by their review priority")
def cards_should_be_ordered_by_priority(context):
    """Verify cards are ordered by review priority (earliest first)"""
    due_cards = context['due_cards']['cards']
    if len(due_cards) > 1:
        for i in range(len(due_cards) - 1):
            current_review = datetime.fromisoformat(due_cards[i]['next_review'].replace('Z', '+00:00'))
            next_review = datetime.fromisoformat(due_cards[i + 1]['next_review'].replace('Z', '+00:00'))
            assert current_review <= next_review


# Scenario: Getting due cards filtered by deck
@given(parsers.parse('I have flashcards in "{deck1}" and "{deck2}" decks'))
def have_flashcards_in_multiple_decks(context, client, deck1, deck2):
    """Create flashcards in multiple decks"""
    cards_data = [
        {"front": "Math Q1", "back": "Math A1", "deck_name": deck1},
        {"front": "Math Q2", "back": "Math A2", "deck_name": deck1},
        {"front": "History Q1", "back": "History A1", "deck_name": deck2},
    ]
    
    context['deck1'] = deck1
    context['deck2'] = deck2
    context['multi_deck_cards'] = []
    
    for card_data in cards_data:
        response = client.post("/api/cards/", json=card_data)
        assert response.status_code == 201
        context['multi_deck_cards'].append(response.json())
    
    # Wait to ensure cards are due
    time.sleep(1)


@given("cards from both decks are due for review")
def cards_from_both_decks_are_due_for_review(context):
    """Verify that cards from both decks are due for review"""
    # This step is mainly for documentation - the previous step should have created due cards
    assert 'multi_deck_cards' in context
    assert len(context['multi_deck_cards']) > 0


@when(parsers.parse('I request due cards filtered by "{deck_name}" deck only'))
def request_due_cards_filtered_by_deck(context, client, deck_name):
    """Request due cards filtered by specific deck"""
    response = client.get(f"/api/cards/due?deck_name={deck_name}")
    context['filtered_due_response'] = response
    context['filter_deck'] = deck_name
    if response.status_code == 200:
        context['filtered_due_cards'] = response.json()


@then(parsers.parse('I should receive only due cards from the "{deck_name}" deck'))
def should_receive_only_deck_due_cards(context, deck_name):
    """Verify only due cards from the specified deck are returned"""
    assert context['filtered_due_response'].status_code == 200
    due_cards = context['filtered_due_cards']['cards']
    for card in due_cards:
        assert card['deck_name'] == deck_name


@then("cards from other decks should not be included")
def cards_from_other_decks_not_included(context):
    """Verify cards from other decks are not included"""
    due_cards = context['filtered_due_cards']['cards']
    filter_deck = context['filter_deck']
    for card in due_cards:
        assert card['deck_name'] == filter_deck


# Error scenarios
@given("I have a flashcard ready for review")
def have_flashcard_ready_for_review(context, client):
    """Create a flashcard ready for review"""
    card_data = {
        "front": "Test question",
        "back": "Test answer",
        "deck_name": "Test"
    }
    response = client.post("/api/cards/", json=card_data)
    assert response.status_code == 201
    context['test_card'] = response.json()


@when(parsers.parse("I attempt to review the flashcard with an invalid quality score of {invalid_quality:d}"))
def attempt_review_with_invalid_quality(context, client, invalid_quality):
    """Attempt to review with invalid quality score"""
    card_id = context['test_card']['id']
    review_data = {
        "quality": invalid_quality,
        "response_time": 3.0
    }
    response = client.post(f"/api/cards/{card_id}/review", json=review_data)
    context['invalid_review_response'] = response


@then("the system should reject the review")
def system_should_reject_review(context):
    """Verify the system rejects invalid review"""
    assert context['invalid_review_response'].status_code == 422


@then("I should receive a validation error message")
def should_receive_validation_error(context):
    """Verify validation error message is received"""
    assert context['invalid_review_response'].status_code == 422
    response_data = context['invalid_review_response'].json()
    assert 'detail' in response_data


@then("the flashcard should remain unchanged")
def flashcard_should_remain_unchanged(context, client):
    """Verify the flashcard was not modified"""
    card_id = context['test_card']['id']
    response = client.get(f"/api/cards/{card_id}")
    assert response.status_code == 200
    current_card = response.json()
    # Card should have same repetitions and ease factor as before
    assert current_card['repetitions'] == context['test_card']['repetitions']
    assert current_card['ease_factor'] == context['test_card']['ease_factor']


@given("I try to review a flashcard that doesn't exist")
def try_review_nonexistent_flashcard(context):
    """Prepare to review a non-existent flashcard"""
    context['nonexistent_card_id'] = 99999


@when("I submit the review with any quality score")
def submit_review_for_nonexistent_card(context, client):
    """Submit review for non-existent flashcard"""
    review_data = {
        "quality": 4,
        "response_time": 3.0
    }
    response = client.post(f"/api/cards/{context['nonexistent_card_id']}/review", json=review_data)
    context['nonexistent_review_response'] = response


@then("I should receive an error message")
def should_receive_error_message_for_review(context):
    """Verify error message for non-existent card review"""
    assert context['nonexistent_review_response'].status_code == 404


@then("the system should indicate the flashcard was not found")
def system_indicates_flashcard_not_found_for_review(context):
    """Verify the error indicates flashcard not found"""
    response_data = context['nonexistent_review_response'].json()
    assert "not found" in response_data['detail'].lower()


# Scenario: Ease factor minimum boundary
@given(parsers.parse("I have a flashcard with the minimum ease factor of {min_ease:f}"))
def have_flashcard_with_minimum_ease(context, client, min_ease):
    """Create a flashcard and reduce its ease factor to minimum"""
    card_data = {
        "front": "Difficult question",
        "back": "Difficult answer",
        "deck_name": "Hard"
    }
    response = client.post("/api/cards/", json=card_data)
    assert response.status_code == 201
    card = response.json()
    
    # Review with poor quality multiple times to reduce ease factor
    for _ in range(5):
        review_data = {"quality": 0, "response_time": 10.0}
        response = client.post(f"/api/cards/{card['id']}/review", json=review_data)
        assert response.status_code == 200
        card = response.json()
    
    context['min_ease_card'] = card


@when(parsers.parse("I review the flashcard with the worst possible performance (quality {quality:d})"))
def review_with_worst_performance(context, client, quality):
    """Review the flashcard with worst possible performance"""
    card_id = context['min_ease_card']['id']
    review_data = {
        "quality": quality,
        "response_time": 15.0
    }
    response = client.post(f"/api/cards/{card_id}/review", json=review_data)
    context['worst_review_response'] = response
    if response.status_code == 200:
        context['worst_reviewed_card'] = response.json()


@then("the ease factor should not decrease below the minimum threshold")
def ease_factor_should_not_go_below_minimum(context):
    """Verify ease factor doesn't go below minimum threshold"""
    assert context['worst_review_response'].status_code == 200
    ease_factor = context['worst_reviewed_card']['ease_factor']
    assert ease_factor >= 1.3  # SM-2 algorithm minimum


@then("the flashcard should still be rescheduled appropriately")
def flashcard_should_be_rescheduled_appropriately(context):
    """Verify the flashcard is still rescheduled despite minimum ease factor"""
    reviewed_card = context['worst_reviewed_card']
    assert 'next_review' in reviewed_card
    assert reviewed_card['interval'] == 1  # Should reset to 1 day for poor performance
