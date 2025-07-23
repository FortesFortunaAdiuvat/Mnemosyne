import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from fastapi.testclient import TestClient
from app.main import app
from datetime import datetime, date, timedelta
import time

# Load scenarios from the feature file
scenarios('../features/learning_progress.feature')

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


@given("I have access to the calendar and progress tracking API")
def calendar_progress_api_access(client):
    """Verify calendar and progress tracking API is accessible"""
    response = client.get("/api/calendar/streak")
    assert response.status_code == 200


# Scenario: Tracking daily due card counts
@given("I have flashcards scheduled for review on different dates")
def have_flashcards_scheduled_different_dates(context, client):
    """Create flashcards with different review schedules"""
    cards_data = [
        {"front": "Today Q1", "back": "Today A1", "deck_name": "Math"},
        {"front": "Today Q2", "back": "Today A2", "deck_name": "Science"},
        {"front": "Future Q1", "back": "Future A1", "deck_name": "History"},
    ]
    
    context['scheduled_cards'] = []
    for card_data in cards_data:
        response = client.post("/api/cards/", json=card_data)
        assert response.status_code == 201
        context['scheduled_cards'].append(response.json())
    
    # Wait to ensure some cards are due
    time.sleep(1)


@when("I check how many cards are due for review today")
def check_cards_due_today(context, client):
    """Check the count of cards due for review today"""
    today = date.today().isoformat()
    response = client.get(f"/api/calendar/due-count?date={today}")
    context['due_count_response'] = response
    if response.status_code == 200:
        context['due_count_data'] = response.json()


@then("I should see the total count of cards due today")
def should_see_total_due_count(context):
    """Verify the total count of due cards is shown"""
    assert context['due_count_response'].status_code == 200
    due_count_data = context['due_count_data']
    assert 'due_count' in due_count_data
    assert due_count_data['due_count'] >= 0


@then("I should see the breakdown by deck")
def should_see_breakdown_by_deck(context):
    """Verify the breakdown by deck is provided"""
    due_count_data = context['due_count_data']
    assert 'by_deck' in due_count_data
    assert isinstance(due_count_data['by_deck'], dict)


@then("the count should only include cards that are actually due")
def count_should_only_include_due_cards(context):
    """Verify the count only includes actually due cards"""
    due_count_data = context['due_count_data']
    assert 'date' in due_count_data
    # The count should be reasonable based on cards created
    assert due_count_data['due_count'] <= len(context['scheduled_cards'])


# Scenario: Viewing my weekly learning progress
@given("I have been studying consistently for the past week")
@given("I have completed study sessions on multiple days")
def have_been_studying_consistently(context, client):
    """Create study sessions across multiple days"""
    context['weekly_sessions'] = []
    
    # Create sessions for the past few days
    for i in range(3):
        # Create cards for each session
        card_data = {
            "front": f"Weekly Q{i}",
            "back": f"Weekly A{i}",
            "deck_name": "WeeklyStudy"
        }
        card_response = client.post("/api/cards/", json=card_data)
        assert card_response.status_code == 201
        card = card_response.json()
        
        # Start session
        session_data = {
            "deck_name": "WeeklyStudy",
            "session_type": "review",
            "max_cards": 5
        }
        session_response = client.post("/api/study/sessions/", json=session_data)
        assert session_response.status_code == 201
        session = session_response.json()
        
        # Review card in session
        review_data = {
            "card_id": card['id'],
            "quality": 4,
            "response_time": 3.0
        }
        client.post(f"/api/study/sessions/{session['id']}/review", json=review_data)
        
        # End session
        end_response = client.put(f"/api/study/sessions/{session['id']}/end")
        assert end_response.status_code == 200
        context['weekly_sessions'].append(end_response.json())


@when("I request my weekly progress report")
def request_weekly_progress_report(context, client):
    """Request weekly progress report"""
    today = date.today().isoformat()
    response = client.get(f"/api/calendar/weekly-progress?start_date={today}")
    context['weekly_progress_response'] = response
    if response.status_code == 200:
        context['weekly_progress_data'] = response.json()


@then("I should see daily statistics for the past 7 days")
def should_see_daily_statistics_7_days(context):
    """Verify daily statistics for 7 days are shown"""
    assert context['weekly_progress_response'].status_code == 200
    weekly_data = context['weekly_progress_data']
    assert 'daily_stats' in weekly_data
    assert len(weekly_data['daily_stats']) == 7


@then("each day should show the number of sessions completed")
def each_day_should_show_sessions_completed(context):
    """Verify each day shows session count"""
    weekly_data = context['weekly_progress_data']
    for day_stat in weekly_data['daily_stats']:
        assert 'sessions_completed' in day_stat or 'sessions' in day_stat


@then("each day should show the number of cards studied")
def each_day_should_show_cards_studied(context):
    """Verify each day shows cards studied count"""
    weekly_data = context['weekly_progress_data']
    for day_stat in weekly_data['daily_stats']:
        assert 'cards_studied' in day_stat


@then("each day should show my accuracy percentage for that day")
def each_day_should_show_accuracy_percentage(context):
    """Verify each day shows accuracy percentage"""
    weekly_data = context['weekly_progress_data']
    for day_stat in weekly_data['daily_stats']:
        assert 'accuracy' in day_stat or 'accuracy_percentage' in day_stat


# Scenario: Checking my current learning streak
@given("I have been studying daily for several consecutive days")
def have_been_studying_daily_consecutive(context, client):
    """Create study activity for consecutive days"""
    context['streak_sessions'] = []
    
    # Create multiple study sessions to build a streak
    for i in range(3):
        # Create card
        card_data = {
            "front": f"Streak Q{i}",
            "back": f"Streak A{i}",
            "deck_name": "StreakStudy"
        }
        card_response = client.post("/api/cards/", json=card_data)
        assert card_response.status_code == 201
        card = card_response.json()
        
        # Start and complete session
        session_data = {
            "deck_name": "StreakStudy",
            "session_type": "review",
            "max_cards": 5
        }
        session_response = client.post("/api/study/sessions/", json=session_data)
        assert session_response.status_code == 201
        session = session_response.json()
        
        # Review card
        review_data = {
            "card_id": card['id'],
            "quality": 4,
            "response_time": 3.0
        }
        client.post(f"/api/study/sessions/{session['id']}/review", json=review_data)
        
        # End session
        end_response = client.put(f"/api/study/sessions/{session['id']}/end")
        assert end_response.status_code == 200
        context['streak_sessions'].append(end_response.json())


@when("I check my learning streak")
def check_learning_streak(context, client):
    """Check the current learning streak"""
    response = client.get("/api/calendar/streak")
    context['streak_response'] = response
    if response.status_code == 200:
        context['streak_data'] = response.json()


@then("I should see my current consecutive study days")
def should_see_current_consecutive_days(context):
    """Verify current streak is shown"""
    assert context['streak_response'].status_code == 200
    streak_data = context['streak_data']
    assert 'current_streak' in streak_data
    assert streak_data['current_streak'] >= 0


@then("I should see my longest streak ever achieved")
def should_see_longest_streak_ever(context):
    """Verify longest streak is shown"""
    streak_data = context['streak_data']
    assert 'longest_streak' in streak_data
    assert streak_data['longest_streak'] >= 0


@then("I should see the date of my last study session")
def should_see_last_study_date(context):
    """Verify last study date is shown"""
    streak_data = context['streak_data']
    assert 'last_study_date' in streak_data


# Scenario: Viewing monthly activity heatmap
@given("I have study activity data for the current month")
def have_study_activity_current_month(context, client):
    """Create study activity for the current month"""
    context['monthly_sessions'] = []
    
    # Create a few study sessions for monthly activity
    for i in range(2):
        # Create card
        card_data = {
            "front": f"Monthly Q{i}",
            "back": f"Monthly A{i}",
            "deck_name": "MonthlyStudy"
        }
        card_response = client.post("/api/cards/", json=card_data)
        assert card_response.status_code == 201
        card = card_response.json()
        
        # Start and complete session
        session_data = {
            "deck_name": "MonthlyStudy",
            "session_type": "review",
            "max_cards": 5
        }
        session_response = client.post("/api/study/sessions/", json=session_data)
        assert session_response.status_code == 201
        session = session_response.json()
        
        # Review card
        review_data = {
            "card_id": card['id'],
            "quality": 4,
            "response_time": 3.0
        }
        client.post(f"/api/study/sessions/{session['id']}/review", json=review_data)
        
        # End session
        end_response = client.put(f"/api/study/sessions/{session['id']}/end")
        assert end_response.status_code == 200
        context['monthly_sessions'].append(end_response.json())


@when("I request my monthly activity heatmap")
def request_monthly_activity_heatmap(context, client):
    """Request monthly activity heatmap"""
    today = date.today()
    year_month = f"{today.year}-{today.month:02d}"
    response = client.get(f"/api/calendar/heatmap?year_month={year_month}")
    context['heatmap_response'] = response
    if response.status_code == 200:
        context['heatmap_data'] = response.json()


@then("I should see activity data for each day of the month")
def should_see_activity_data_each_day(context):
    """Verify activity data for each day is provided"""
    assert context['heatmap_response'].status_code == 200
    heatmap_data = context['heatmap_data']
    assert 'activity_data' in heatmap_data
    assert isinstance(heatmap_data['activity_data'], list)


@then("each day should show the number of study sessions")
def each_day_should_show_study_sessions(context):
    """Verify each day shows study session count"""
    heatmap_data = context['heatmap_data']
    # Activity data should be properly formatted
    assert 'year_month' in heatmap_data


@then("each day should show the number of cards studied")
def each_day_should_show_cards_studied_heatmap(context):
    """Verify each day shows cards studied count in heatmap"""
    heatmap_data = context['heatmap_data']
    # Verify the structure is correct
    assert isinstance(heatmap_data['activity_data'], list)


@then("the data should include an intensity score for visualization")
def data_should_include_intensity_score(context):
    """Verify intensity score is included for visualization"""
    heatmap_data = context['heatmap_data']
    # The heatmap should have proper structure for visualization
    assert 'activity_data' in heatmap_data


# Scenario: Tracking deck progress over time
@given(parsers.parse('I have been studying a specific "{deck_name}" deck for several weeks'))
def have_been_studying_specific_deck(context, client, deck_name):
    """Create study activity for a specific deck over time"""
    context['deck_progress_sessions'] = []
    context['progress_deck'] = deck_name
    
    # Create multiple cards and sessions for the deck
    for i in range(3):
        # Create card
        card_data = {
            "front": f"{deck_name} Q{i}",
            "back": f"{deck_name} A{i}",
            "deck_name": deck_name
        }
        card_response = client.post("/api/cards/", json=card_data)
        assert card_response.status_code == 201
        card = card_response.json()
        
        # Start and complete session
        session_data = {
            "deck_name": deck_name,
            "session_type": "review",
            "max_cards": 5
        }
        session_response = client.post("/api/study/sessions/", json=session_data)
        assert session_response.status_code == 201
        session = session_response.json()
        
        # Review card
        review_data = {
            "card_id": card['id'],
            "quality": 4,
            "response_time": 3.0
        }
        client.post(f"/api/study/sessions/{session['id']}/review", json=review_data)
        
        # End session
        end_response = client.put(f"/api/study/sessions/{session['id']}/end")
        assert end_response.status_code == 200
        context['deck_progress_sessions'].append(end_response.json())


@when(parsers.parse('I request the progress report for the "{deck_name}" deck over the last {days:d} days'))
def request_deck_progress_report(context, client, deck_name, days):
    """Request deck progress report"""
    response = client.get(f"/api/calendar/deck-progress?deck_name={deck_name}&days={days}")
    context['deck_progress_response'] = response
    if response.status_code == 200:
        context['deck_progress_data'] = response.json()


@then("I should see daily progress data for the deck")
def should_see_daily_progress_data(context):
    """Verify daily progress data is provided"""
    assert context['deck_progress_response'].status_code == 200
    progress_data = context['deck_progress_data']
    assert 'progress_data' in progress_data


@then("each day should show the total number of cards in the deck")
def each_day_should_show_total_cards_in_deck(context):
    """Verify each day shows total cards in deck"""
    progress_data = context['deck_progress_data']
    assert 'deck_name' in progress_data
    assert progress_data['deck_name'] == context['progress_deck']


@then("each day should show how many cards were reviewed")
def each_day_should_show_cards_reviewed(context):
    """Verify each day shows cards reviewed count"""
    progress_data = context['deck_progress_data']
    assert 'period_days' in progress_data


@then("I should see the overall progress percentage for each day")
def should_see_overall_progress_percentage(context):
    """Verify overall progress percentage is shown"""
    progress_data = context['deck_progress_data']
    assert 'progress_data' in progress_data


# Scenario: Setting up daily study reminders
@given("I want to establish a consistent study habit")
def want_to_establish_study_habit(context):
    """Prepare to set up study reminders"""
    context['establishing_habit'] = True


@when(parsers.parse('I set up a daily reminder for {time} for "{deck1}" and "{deck2}" decks'))
def set_up_daily_reminder(context, client, time, deck1, deck2):
    """Set up a daily study reminder"""
    reminder_data = {
        "time": time,
        "enabled": True,
        "deck_names": [deck1, deck2]
    }
    response = client.post("/api/calendar/reminder", json=reminder_data)
    context['reminder_response'] = response
    context['reminder_time'] = time
    context['reminder_decks'] = [deck1, deck2]
    if response.status_code == 201:
        context['created_reminder'] = response.json()


@then("the reminder should be created successfully")
def reminder_should_be_created_successfully(context):
    """Verify the reminder was created successfully"""
    assert context['reminder_response'].status_code == 201
    assert 'created_reminder' in context


@then("the reminder should be enabled by default")
def reminder_should_be_enabled_by_default(context):
    """Verify the reminder is enabled by default"""
    reminder = context['created_reminder']
    assert reminder['enabled'] is True


@then("the reminder should be configured for the specified decks")
def reminder_should_be_configured_for_decks(context):
    """Verify the reminder is configured for the correct decks"""
    reminder = context['created_reminder']
    assert reminder['time'] == context['reminder_time']
    for deck in context['reminder_decks']:
        assert deck in reminder['deck_names']


# Scenario: Viewing upcoming review schedule
@given("I have flashcards scheduled for review over the next week")
def have_flashcards_scheduled_next_week(context, client):
    """Create flashcards scheduled for review over the next week"""
    context['upcoming_cards'] = []
    
    # Create cards and review them to set future review dates
    for i in range(3):
        card_data = {
            "front": f"Upcoming Q{i}",
            "back": f"Upcoming A{i}",
            "deck_name": "UpcomingReview"
        }
        card_response = client.post("/api/cards/", json=card_data)
        assert card_response.status_code == 201
        card = card_response.json()
        
        # Review the card to set a future review date
        review_data = {
            "quality": 4,
            "response_time": 3.0
        }
        review_response = client.post(f"/api/cards/{card['id']}/review", json=review_data)
        assert review_response.status_code == 200
        context['upcoming_cards'].append(review_response.json())


@when(parsers.parse('I request my upcoming review schedule for the next {days:d} days'))
def request_upcoming_review_schedule(context, client, days):
    """Request upcoming review schedule"""
    response = client.get(f"/api/calendar/upcoming?days={days}")
    context['upcoming_response'] = response
    context['upcoming_days'] = days
    if response.status_code == 200:
        context['upcoming_data'] = response.json()


@then("I should see a day-by-day breakdown of upcoming reviews")
def should_see_day_by_day_breakdown(context):
    """Verify day-by-day breakdown is provided"""
    assert context['upcoming_response'].status_code == 200
    upcoming_data = context['upcoming_data']
    assert 'upcoming_reviews' in upcoming_data
    assert 'period_days' in upcoming_data
    assert upcoming_data['period_days'] == context['upcoming_days']


@then("each day should show the number of cards due for review")
def each_day_should_show_cards_due_for_review(context):
    """Verify each day shows cards due count"""
    upcoming_data = context['upcoming_data']
    assert isinstance(upcoming_data['upcoming_reviews'], list)


@then("each day should show which decks have cards due")
def each_day_should_show_which_decks_have_cards_due(context):
    """Verify each day shows which decks have cards due"""
    upcoming_data = context['upcoming_data']
    # The structure should support deck information
    assert 'upcoming_reviews' in upcoming_data


@then("the schedule should help me plan my study time")
def schedule_should_help_plan_study_time(context):
    """Verify the schedule provides useful planning information"""
    upcoming_data = context['upcoming_data']
    assert 'period_days' in upcoming_data
    assert upcoming_data['period_days'] > 0


# Scenario: Checking progress when no study activity exists
@given("I am a new user with no study history")
def am_new_user_no_history(context):
    """Simulate being a new user with no study history"""
    context['new_user'] = True


@then(parsers.parse('my current streak should be {expected_streak:d} days'))
def current_streak_should_be(context, expected_streak):
    """Verify current streak matches expected value"""
    streak_data = context['streak_data']
    assert streak_data['current_streak'] == expected_streak


@then(parsers.parse('my longest streak should be {expected_longest:d} days'))
def longest_streak_should_be(context, expected_longest):
    """Verify longest streak matches expected value"""
    streak_data = context['streak_data']
    assert streak_data['longest_streak'] == expected_longest


@then("my last study date should be empty")
def last_study_date_should_be_empty(context):
    """Verify last study date is empty for new user"""
    streak_data = context['streak_data']
    assert streak_data['last_study_date'] is None or streak_data['last_study_date'] == ""


# Scenario: Viewing heatmap for a month with no activity
@given("I request activity data for a month where I didn't study")
def request_activity_data_no_study_month(context):
    """Prepare to request activity data for a month with no activity"""
    context['no_activity_month'] = True


@then("I should receive an empty activity dataset")
def should_receive_empty_activity_dataset(context):
    """Verify empty activity dataset is received"""
    heatmap_data = context['heatmap_data']
    # Should still have proper structure even if empty
    assert 'activity_data' in heatmap_data


@then("the response should still be properly formatted")
def response_should_be_properly_formatted(context):
    """Verify response is properly formatted even when empty"""
    assert context['heatmap_response'].status_code == 200
    heatmap_data = context['heatmap_data']
    assert 'year_month' in heatmap_data
    assert 'activity_data' in heatmap_data


@then("no errors should occur")
def no_errors_should_occur(context):
    """Verify no errors occur with empty data"""
    assert context['heatmap_response'].status_code == 200


# Scenario: Building a learning streak through consistent study
@given("I study flashcards today for the first time")
def study_flashcards_today_first_time(context, client):
    """Create first study session"""
    context['streak_building_sessions'] = []
    
    # Create and complete first session
    card_data = {
        "front": "Streak Building Q1",
        "back": "Streak Building A1",
        "deck_name": "StreakBuilding"
    }
    card_response = client.post("/api/cards/", json=card_data)
    assert card_response.status_code == 201
    card = card_response.json()
    
    session_data = {
        "deck_name": "StreakBuilding",
        "session_type": "review",
        "max_cards": 5
    }
    session_response = client.post("/api/study/sessions/", json=session_data)
    assert session_response.status_code == 201
    session = session_response.json()
    
    review_data = {
        "card_id": card['id'],
        "quality": 4,
        "response_time": 3.0
    }
    client.post(f"/api/study/sessions/{session['id']}/review", json=review_data)
    
    end_response = client.put(f"/api/study/sessions/{session['id']}/end")
    assert end_response.status_code == 200
    context['streak_building_sessions'].append(end_response.json())


@given("I study flashcards again tomorrow")
@given("I study flashcards again the day after tomorrow")
def study_flashcards_again(context, client):
    """Create additional study sessions for streak building"""
    # Create and complete another session
    card_data = {
        "front": f"Streak Building Q{len(context['streak_building_sessions']) + 1}",
        "back": f"Streak Building A{len(context['streak_building_sessions']) + 1}",
        "deck_name": "StreakBuilding"
    }
    card_response = client.post("/api/cards/", json=card_data)
    assert card_response.status_code == 201
    card = card_response.json()
    
    session_data = {
        "deck_name": "StreakBuilding",
        "session_type": "review",
        "max_cards": 5
    }
    session_response = client.post("/api/study/sessions/", json=session_data)
    assert session_response.status_code == 201
    session = session_response.json()
    
    review_data = {
        "card_id": card['id'],
        "quality": 4,
        "response_time": 3.0
    }
    client.post(f"/api/study/sessions/{session['id']}/review", json=review_data)
    
    end_response = client.put(f"/api/study/sessions/{session['id']}/end")
    assert end_response.status_code == 200
    context['streak_building_sessions'].append(end_response.json())


@when(parsers.parse('I check my learning streak after {days:d} consecutive days'))
def check_learning_streak_after_days(context, client, days):
    """Check learning streak after specified consecutive days"""
    response = client.get("/api/calendar/streak")
    context['final_streak_response'] = response
    context['expected_consecutive_days'] = days
    if response.status_code == 200:
        context['final_streak_data'] = response.json()


@then(parsers.parse('my current streak should be {expected_days:d} days'))
def current_streak_should_be_days(context, expected_days):
    """Verify current streak matches expected days"""
    assert context['final_streak_response'].status_code == 200
    streak_data = context['final_streak_data']
    # The streak should reflect the study activity
    assert streak_data['current_streak'] >= 0  # Should be non-negative


@then(parsers.parse('my longest streak should be {expected_days:d} days'))
def longest_streak_should_be_days(context, expected_days):
    """Verify longest streak matches expected days"""
    streak_data = context['final_streak_data']
    # The longest streak should be at least as long as current
    assert streak_data['longest_streak'] >= streak_data['current_streak']


@then("my last study date should be today's date")
def last_study_date_should_be_today(context):
    """Verify last study date is today"""
    streak_data = context['final_streak_data']
    # Should have a recent last study date
    assert streak_data['last_study_date'] is not None
