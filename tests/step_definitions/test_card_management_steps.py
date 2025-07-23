import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from fastapi.testclient import TestClient
from app.main import app

# Load scenarios from the feature file
scenarios('../features/card_management.feature')

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


@given("I have access to the card management API")
def card_management_api_access(client):
    """Verify card management API is accessible"""
    response = client.get("/api/cards/")
    assert response.status_code == 200


# Scenario: Creating a new flashcard
@given(parsers.parse('I want to learn about "{deck_name}"'))
def want_to_learn_about_deck(context, deck_name):
    """Set the deck name for learning"""
    context['deck_name'] = deck_name


@when(parsers.parse('I create a flashcard with question "{question}" and answer "{answer}"'))
def create_flashcard_with_question_and_answer(context, client, question, answer):
    """Create a flashcard with specified question and answer"""
    card_data = {
        "front": question,
        "back": answer,
        "deck_name": context.get('deck_name', 'default')
    }
    response = client.post("/api/cards/", json=card_data)
    context['response'] = response
    context['card_data'] = card_data
    if response.status_code == 201:
        context['created_card'] = response.json()


@then("the flashcard should be saved successfully")
def flashcard_saved_successfully(context):
    """Verify the flashcard was saved successfully"""
    assert context['response'].status_code == 201
    assert 'created_card' in context


@then(parsers.parse('the flashcard should be assigned to the "{deck_name}" deck'))
def flashcard_assigned_to_deck(context, deck_name):
    """Verify the flashcard is assigned to the correct deck"""
    assert context['created_card']['deck_name'] == deck_name


@then("the flashcard should be immediately available for review")
def flashcard_available_for_review(context):
    """Verify the flashcard is available for review"""
    card = context['created_card']
    assert 'next_review' in card
    assert card['repetitions'] == 0
    assert card['ease_factor'] == 2.5


# Scenario: Creating a flashcard without specifying a deck
@given("I want to create a basic flashcard")
def want_to_create_basic_flashcard(context):
    """Prepare to create a basic flashcard"""
    context['basic_card'] = True


@when(parsers.parse('I create a flashcard with question "{question}" and answer "{answer}" without specifying a deck'))
def create_flashcard_without_deck(context, client, question, answer):
    """Create a flashcard without specifying a deck"""
    card_data = {
        "front": question,
        "back": answer
    }
    response = client.post("/api/cards/", json=card_data)
    context['response'] = response
    if response.status_code == 201:
        context['created_card'] = response.json()


@then(parsers.parse('the flashcard should be assigned to the "{default_deck}" deck'))
def flashcard_assigned_to_default_deck(context, default_deck):
    """Verify the flashcard is assigned to the default deck"""
    assert context['created_card']['deck_name'] == default_deck


# Scenario: Viewing my flashcard collection
@given("I have created several flashcards in different decks")
def created_several_flashcards(context, client):
    """Create several flashcards in different decks"""
    cards = [
        {"front": "Q1", "back": "A1", "deck_name": "Math"},
        {"front": "Q2", "back": "A2", "deck_name": "Science"},
        {"front": "Q3", "back": "A3", "deck_name": "Math"},
    ]
    context['created_cards'] = []
    for card_data in cards:
        response = client.post("/api/cards/", json=card_data)
        if response.status_code == 201:
            context['created_cards'].append(response.json())


@when("I request to view my flashcard collection")
def request_flashcard_collection(context, client):
    """Request to view the flashcard collection"""
    response = client.get("/api/cards/")
    context['response'] = response
    if response.status_code == 200:
        context['collection'] = response.json()


@then("I should see all my flashcards")
def should_see_all_flashcards(context):
    """Verify all flashcards are visible"""
    assert context['response'].status_code == 200
    assert len(context['collection']['cards']) >= len(context['created_cards'])


@then("the results should be paginated for easy browsing")
def results_should_be_paginated(context):
    """Verify pagination information is present"""
    collection = context['collection']
    assert 'page' in collection
    assert 'size' in collection
    assert 'pages' in collection


@then("I should see the total count of my flashcards")
def should_see_total_count(context):
    """Verify total count is provided"""
    assert 'total' in context['collection']
    assert context['collection']['total'] >= 0


# Scenario: Filtering flashcards by deck
@given(parsers.parse('I have flashcards in "{deck1}" and "{deck2}" decks'))
def have_flashcards_in_decks(context, client, deck1, deck2):
    """Create flashcards in specified decks"""
    cards = [
        {"front": "Math Q1", "back": "Math A1", "deck_name": deck1},
        {"front": "Science Q1", "back": "Science A1", "deck_name": deck2},
    ]
    context['deck1'] = deck1
    context['deck2'] = deck2
    for card_data in cards:
        client.post("/api/cards/", json=card_data)


@when(parsers.parse('I filter my flashcards to show only "{deck_name}" deck'))
def filter_flashcards_by_deck(context, client, deck_name):
    """Filter flashcards by deck name"""
    response = client.get(f"/api/cards/?deck_name={deck_name}")
    context['response'] = response
    context['filtered_deck'] = deck_name
    if response.status_code == 200:
        context['filtered_cards'] = response.json()


@then(parsers.parse('I should see only flashcards from the "{deck_name}" deck'))
def should_see_only_deck_flashcards(context, deck_name):
    """Verify only flashcards from the specified deck are shown"""
    assert context['response'].status_code == 200
    cards = context['filtered_cards']['cards']
    for card in cards:
        assert card['deck_name'] == deck_name


@then("flashcards from other decks should not be shown")
def flashcards_from_other_decks_not_shown(context):
    """Verify flashcards from other decks are not shown"""
    cards = context['filtered_cards']['cards']
    filtered_deck = context['filtered_deck']
    for card in cards:
        assert card['deck_name'] == filtered_deck


# Scenario: Updating a flashcard
@given(parsers.parse('I have a flashcard with question "{question}" and answer "{answer}"'))
def have_flashcard_with_content(context, client, question, answer):
    """Create a flashcard with specific content"""
    card_data = {"front": question, "back": answer}
    response = client.post("/api/cards/", json=card_data)
    assert response.status_code == 201
    context['original_card'] = response.json()


@when(parsers.parse('I update the question to "{new_question}" and answer to "{new_answer}"'))
def update_flashcard_content(context, client, new_question, new_answer):
    """Update the flashcard content"""
    card_id = context['original_card']['id']
    update_data = {"front": new_question, "back": new_answer}
    response = client.put(f"/api/cards/{card_id}", json=update_data)
    context['response'] = response
    if response.status_code == 200:
        context['updated_card'] = response.json()


@then("the flashcard should be updated successfully")
def flashcard_updated_successfully(context):
    """Verify the flashcard was updated successfully"""
    assert context['response'].status_code == 200


@then("the new content should be saved")
def new_content_should_be_saved(context):
    """Verify the new content is saved"""
    updated_card = context['updated_card']
    assert updated_card['front'] != context['original_card']['front']
    assert updated_card['back'] != context['original_card']['back']


# Scenario: Deleting a flashcard
@given("I have a flashcard I no longer need")
def have_flashcard_to_delete(context, client):
    """Create a flashcard to delete"""
    card_data = {"front": "Delete me", "back": "I will be deleted"}
    response = client.post("/api/cards/", json=card_data)
    assert response.status_code == 201
    context['card_to_delete'] = response.json()


@when("I delete the flashcard")
def delete_flashcard(context, client):
    """Delete the flashcard"""
    card_id = context['card_to_delete']['id']
    response = client.delete(f"/api/cards/{card_id}")
    context['response'] = response


@then("the flashcard should be removed from my collection")
def flashcard_removed_from_collection(context):
    """Verify the flashcard was removed"""
    assert context['response'].status_code == 204


@then("it should no longer appear in my flashcard list")
def flashcard_not_in_list(context, client):
    """Verify the flashcard doesn't appear in the list"""
    card_id = context['card_to_delete']['id']
    response = client.get(f"/api/cards/{card_id}")
    assert response.status_code == 404


# Error scenarios
@given("I try to update a flashcard that doesn't exist")
def try_update_nonexistent_flashcard(context):
    """Prepare to update a non-existent flashcard"""
    context['nonexistent_card_id'] = 99999


@when("I submit the update request")
def submit_update_request(context, client):
    """Submit update request for non-existent flashcard"""
    update_data = {"front": "Updated", "back": "Updated"}
    response = client.put(f"/api/cards/{context['nonexistent_card_id']}", json=update_data)
    context['response'] = response


@then("I should receive an error message")
def should_receive_error_message(context):
    """Verify error message is received"""
    assert context['response'].status_code == 404


@then("the system should indicate the flashcard was not found")
def system_indicates_flashcard_not_found(context):
    """Verify the error indicates flashcard not found"""
    response_data = context['response'].json()
    assert "not found" in response_data['detail'].lower()


@given("I try to delete a flashcard that doesn't exist")
def try_delete_nonexistent_flashcard(context):
    """Prepare to delete a non-existent flashcard"""
    context['nonexistent_card_id'] = 99999


@when("I submit the delete request")
def submit_delete_request(context, client):
    """Submit delete request for non-existent flashcard"""
    response = client.delete(f"/api/cards/{context['nonexistent_card_id']}")
    context['response'] = response
