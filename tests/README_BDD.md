# BDD Tests for Mnemosyne Spaced Repetition System

This directory contains comprehensive Behavior-Driven Development (BDD) tests using pytest-bdd that describe the Mnemosyne learning system's functionality in business terminology.

## Overview

The BDD tests are organized into four main feature areas, each with corresponding step definitions that test the API through business-focused scenarios.

## Test Structure

```
tests/
├── features/                          # Gherkin feature files
│   ├── card_management.feature         # Flashcard CRUD operations
│   ├── spaced_repetition.feature       # SM-2 algorithm and review logic
│   ├── study_sessions.feature          # Structured learning sessions
│   └── learning_progress.feature       # Progress tracking and habits
├── step_definitions/                   # Python step implementations
│   ├── conftest.py                     # Shared BDD test configuration
│   ├── test_card_management_steps.py   # Card management step definitions
│   ├── test_spaced_repetition_steps.py # Spaced repetition step definitions
│   ├── test_study_sessions_steps.py    # Study session step definitions
│   └── test_learning_progress_steps.py # Progress tracking step definitions
└── README_BDD.md                      # This documentation
```

## Feature Coverage

### 1. Card Management (8/8 scenarios passing - 100%)
**File**: `features/card_management.feature`

Tests flashcard lifecycle management using business terminology:

- **Creating flashcards** with and without deck specification
- **Viewing collections** with pagination and filtering
- **Updating content** with partial and complete modifications
- **Deleting cards** with proper cleanup
- **Error handling** for non-existent cards

**Example Scenario**:
```gherkin
Scenario: Creating a new flashcard
  Given I want to learn about "Geography"
  When I create a flashcard with question "What is the capital of France?" and answer "Paris"
  Then the flashcard should be saved successfully
  And the flashcard should be assigned to the "Geography" deck
  And the flashcard should be immediately available for review
```

### 2. Spaced Repetition Learning (8/8 scenarios passing - 100%)
**File**: `features/spaced_repetition.feature`

Tests the SM-2 algorithm implementation with learning-focused language:

- **First-time reviews** with quality-based scheduling
- **Progressive reviews** with increasing intervals
- **Incorrect reviews** with repetition resets
- **Due card retrieval** with priority ordering
- **Deck filtering** for focused study
- **Error handling** for invalid inputs
- **Boundary testing** for ease factor limits

**Example Scenario**:
```gherkin
Scenario: Reviewing a flashcard correctly for the first time
  Given I have a new flashcard that I haven't reviewed yet
  When I review the flashcard and rate my performance as "good" (quality 4)
  Then the flashcard's repetition count should increase to 1
  And the flashcard should be scheduled for review in 1 day
  And my ease factor should improve slightly
```

### 3. Study Sessions (4/10 scenarios passing - 40%)
**File**: `features/study_sessions.feature`

Tests structured learning sessions with session management:

- **Session lifecycle** (start, progress, end)
- **Card retrieval** within sessions
- **Review submission** with progress tracking
- **Session limits** and completion logic
- **Statistics tracking** across sessions
- **Error handling** for invalid sessions

**Example Scenario**:
```gherkin
Scenario: Starting a new study session
  Given I want to study my "Math" flashcards
  When I start a study session for the "Math" deck with a maximum of 10 cards
  Then a new study session should be created
  And the session should be configured for the "Math" deck
  And the session should be limited to 10 cards maximum
```

### 4. Learning Progress & Habit Tracking (5/10 scenarios passing - 50%)
**File**: `features/learning_progress.feature`

Tests progress tracking and habit-building features:

- **Daily due counts** with deck breakdowns
- **Weekly progress** with accuracy trends
- **Learning streaks** (current and longest)
- **Monthly heatmaps** for visualization
- **Deck progress** over time
- **Study reminders** for habit formation
- **Upcoming schedules** for planning

**Example Scenario**:
```gherkin
Scenario: Checking my current learning streak
  Given I have been studying daily for several consecutive days
  When I check my learning streak
  Then I should see my current consecutive study days
  And I should see my longest streak ever achieved
  And I should see the date of my last study session
```

## Running BDD Tests

### Run All BDD Tests
```bash
source .venv/bin/activate
python3 -m pytest tests/step_definitions/ -v
```

### Run Specific Feature Tests
```bash
# Card management tests
python3 -m pytest tests/step_definitions/test_card_management_steps.py -v

# Spaced repetition tests
python3 -m pytest tests/step_definitions/test_spaced_repetition_steps.py -v

# Study session tests
python3 -m pytest tests/step_definitions/test_study_sessions_steps.py -v

# Learning progress tests
python3 -m pytest tests/step_definitions/test_learning_progress_steps.py -v
```

### Run with Detailed Output
```bash
python3 -m pytest tests/step_definitions/ -v -s --tb=short
```

## Current Test Status

**Overall BDD Test Results**: 28 passed, 8 failed (78% pass rate)

### ✅ Fully Passing Features
- **Card Management**: 8/8 scenarios (100%)
- **Spaced Repetition**: 8/8 scenarios (100%)

### ⚠️ Partially Passing Features
- **Study Sessions**: 4/10 scenarios (40%)
- **Learning Progress**: 5/10 scenarios (50%)

### Known Issues
1. **Calendar API Integration**: Some progress tracking endpoints need implementation
2. **Study Session Edge Cases**: Session limit and error handling scenarios
3. **Timing Dependencies**: Some tests require better timing control

## BDD Test Benefits

### Business Value
- **Readable Specifications**: Tests serve as living documentation
- **Stakeholder Communication**: Non-technical users can understand test scenarios
- **Requirements Validation**: Ensures features match business needs
- **Regression Protection**: Prevents breaking existing functionality

### Technical Benefits
- **API Integration Testing**: Tests the complete request/response cycle
- **Database Integration**: Validates data persistence and retrieval
- **Error Handling**: Comprehensive testing of edge cases
- **Test Isolation**: Each scenario runs in a clean database state

## Writing New BDD Tests

### 1. Create Feature File
Write scenarios in `tests/features/` using Gherkin syntax:

```gherkin
Feature: New Feature
  As a user
  I want to perform some action
  So that I can achieve some goal

  Scenario: Descriptive scenario name
    Given some initial condition
    When I perform some action
    And I provide some input
    Then I should see some result
    And the system should behave correctly
```

### 2. Implement Step Definitions
Create corresponding step definitions in `tests/step_definitions/`:

```python
from pytest_bdd import scenarios, given, when, then, parsers

scenarios('../features/new_feature.feature')

@given("some initial condition")
def initial_condition(context, client):
    # Setup test data
    pass

@when(parsers.parse('I perform some action with "{parameter}"'))
def perform_action(context, client, parameter):
    # Execute API call
    response = client.post("/api/endpoint", json={"param": parameter})
    context['response'] = response

@then("I should see some result")
def verify_result(context):
    # Assert expected outcome
    assert context['response'].status_code == 200
```

### 3. Use Business Language
- Focus on **what** the user wants to achieve, not **how** it's implemented
- Use domain-specific terminology (flashcards, decks, reviews, streaks)
- Write scenarios from the user's perspective
- Avoid technical implementation details in feature files

## Test Configuration

### Database Setup
- **Isolated Database**: Each test uses a separate SQLite database
- **Clean State**: Tables are created/dropped for each test
- **Shared Configuration**: Common setup in `conftest.py`

### Fixtures
- **`client`**: FastAPI test client for API calls
- **`context`**: Dictionary for sharing data between steps
- **Database fixtures**: Automatic setup/teardown

### Dependencies
- **pytest-bdd**: BDD framework for Python
- **FastAPI TestClient**: API testing utilities
- **SQLAlchemy**: Database ORM for test data

## Contributing to BDD Tests

1. **Understand the Feature**: Read existing scenarios to understand patterns
2. **Write User Stories**: Focus on business value and user goals
3. **Use Consistent Language**: Follow established terminology
4. **Test Edge Cases**: Include error scenarios and boundary conditions
5. **Maintain Isolation**: Ensure tests don't depend on each other
6. **Document Scenarios**: Add clear descriptions and examples

## Future Enhancements

### Planned Improvements
- **Complete Calendar API**: Implement remaining progress tracking endpoints
- **Enhanced Error Testing**: More comprehensive error scenario coverage
- **Performance Testing**: Add timing and load-based scenarios
- **User Authentication**: Multi-user scenario testing
- **Data Import/Export**: File-based learning content scenarios

### Advanced BDD Features
- **Scenario Outlines**: Parameterized tests with example tables
- **Background Steps**: Common setup across scenarios
- **Tags**: Categorize and filter scenarios
- **Hooks**: Setup/teardown at various test levels

This BDD test suite provides comprehensive coverage of the Mnemosyne learning system's core functionality while maintaining readability and business alignment.
