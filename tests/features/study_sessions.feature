Feature: Study Sessions
  As a learner
  I want to conduct structured study sessions
  So that I can focus my learning and track my progress

  Background:
    Given the Mnemosyne learning system is running
    And I have access to the study session API

  Scenario: Starting a new study session
    Given I want to study my "Math" flashcards
    When I start a study session for the "Math" deck with a maximum of 10 cards
    Then a new study session should be created
    And the session should be configured for the "Math" deck
    And the session should be limited to 10 cards maximum
    And the session should show 0 cards studied initially

  Scenario: Getting the next card in an active session
    Given I have an active study session for "Science" deck
    And there are flashcards due for review in the "Science" deck
    When I request the next card to review
    Then I should receive a flashcard from the "Science" deck
    And the session should not be marked as complete
    And the flashcard should be ready for review

  Scenario: Getting next card when no cards are due
    Given I have an active study session for "History" deck
    And there are no flashcards due for review in the "History" deck
    When I request the next card to review
    Then I should receive no flashcard
    And the session should be marked as complete
    And I should be notified that no more cards are available

  Scenario: Reviewing a card within a study session
    Given I have an active study session
    And I have received a flashcard to review
    When I submit my review with quality score 4 and response time 3.5 seconds
    Then the session's cards studied count should increase by 1
    And the session's correct answers count should increase by 1
    And the flashcard should be updated with the new review data

  Scenario: Reviewing a card incorrectly within a session
    Given I have an active study session
    And I have received a flashcard to review
    When I submit my review with quality score 1 and response time 8.0 seconds
    Then the session's cards studied count should increase by 1
    And the session's correct answers count should remain unchanged
    And the flashcard should be rescheduled appropriately

  Scenario: Ending a study session
    Given I have an active study session
    When I end the study session
    Then the session should be marked as complete
    And the session should have an end timestamp
    And I should be able to see my session results

  Scenario: Reaching the maximum card limit in a session
    Given I have a study session limited to 5 cards
    And I have already studied 5 cards in this session
    When I request the next card to review
    Then I should receive no flashcard
    And the session should be marked as complete
    And I should be notified that the session limit has been reached

  Scenario: Viewing my overall study statistics
    Given I have completed several study sessions
    When I request my overall study statistics
    Then I should see the total number of study sessions completed
    And I should see the total number of cards I have studied
    And I should see my average accuracy percentage across all sessions

  Scenario: Attempting to get next card from non-existent session
    Given I try to get the next card from a session that doesn't exist
    When I submit the request
    Then I should receive an error message
    And the system should indicate the session was not found

  Scenario: Attempting to submit review to non-existent session
    Given I try to submit a review to a session that doesn't exist
    When I submit the review request
    Then I should receive an error message
    And the system should indicate the session was not found
