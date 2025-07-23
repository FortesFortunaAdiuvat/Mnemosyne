Feature: Learning Progress and Habit Tracking
  As a learner
  I want to track my learning progress and build study habits
  So that I can monitor my improvement and maintain consistent learning

  Background:
    Given the Mnemosyne learning system is running
    And I have access to the calendar and progress tracking API

  Scenario: Tracking daily due card counts
    Given I have flashcards scheduled for review on different dates
    When I check how many cards are due for review today
    Then I should see the total count of cards due today
    And I should see the breakdown by deck
    And the count should only include cards that are actually due

  Scenario: Viewing my weekly learning progress
    Given I have been studying consistently for the past week
    And I have completed study sessions on multiple days
    When I request my weekly progress report
    Then I should see daily statistics for the past 7 days
    And each day should show the number of sessions completed
    And each day should show the number of cards studied
    And each day should show my accuracy percentage for that day

  Scenario: Checking my current learning streak
    Given I have been studying daily for several consecutive days
    When I check my learning streak
    Then I should see my current consecutive study days
    And I should see my longest streak ever achieved
    And I should see the date of my last study session

  Scenario: Viewing monthly activity heatmap
    Given I have study activity data for the current month
    When I request my monthly activity heatmap
    Then I should see activity data for each day of the month
    And each day should show the number of study sessions
    And each day should show the number of cards studied
    And the data should include an intensity score for visualization

  Scenario: Tracking deck progress over time
    Given I have been studying a specific "Spanish" deck for several weeks
    When I request the progress report for the "Spanish" deck over the last 30 days
    Then I should see daily progress data for the deck
    And each day should show the total number of cards in the deck
    And each day should show how many cards were reviewed
    And I should see the overall progress percentage for each day

  Scenario: Setting up daily study reminders
    Given I want to establish a consistent study habit
    When I set up a daily reminder for 9:00 AM for "Math" and "Science" decks
    Then the reminder should be created successfully
    And the reminder should be enabled by default
    And the reminder should be configured for the specified decks

  Scenario: Viewing upcoming review schedule
    Given I have flashcards scheduled for review over the next week
    When I request my upcoming review schedule for the next 7 days
    Then I should see a day-by-day breakdown of upcoming reviews
    And each day should show the number of cards due for review
    And each day should show which decks have cards due
    And the schedule should help me plan my study time

  Scenario: Checking progress when no study activity exists
    Given I am a new user with no study history
    When I check my learning streak
    Then my current streak should be 0 days
    And my longest streak should be 0 days
    And my last study date should be empty

  Scenario: Viewing heatmap for a month with no activity
    Given I request activity data for a month where I didn't study
    When I request my monthly activity heatmap
    Then I should receive an empty activity dataset
    And the response should still be properly formatted
    And no errors should occur

  Scenario: Building a learning streak through consistent study
    Given I study flashcards today for the first time
    And I study flashcards again tomorrow
    And I study flashcards again the day after tomorrow
    When I check my learning streak after three consecutive days
    Then my current streak should be 3 days
    And my longest streak should be 3 days
    And my last study date should be today's date
