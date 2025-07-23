Feature: Spaced Repetition Learning
  As a learner
  I want to review flashcards using spaced repetition
  So that I can optimize my long-term memory retention

  Background:
    Given the Mnemosyne learning system is running
    And I have access to the spaced repetition API

  Scenario: Reviewing a flashcard correctly for the first time
    Given I have a new flashcard that I haven't reviewed yet
    When I review the flashcard and rate my performance as "good" (quality 4)
    Then the flashcard's repetition count should increase to 1
    And the flashcard should be scheduled for review in 1 day
    And my ease factor should improve slightly

  Scenario: Reviewing a flashcard correctly for the second time
    Given I have a flashcard that I've reviewed correctly once before
    And the flashcard has 1 repetition and ease factor of 2.6
    When I review the flashcard and rate my performance as "perfect" (quality 5)
    Then the flashcard's repetition count should increase to 2
    And the flashcard should be scheduled for review in 6 days
    And my ease factor should improve further

  Scenario: Reviewing a flashcard incorrectly
    Given I have a flashcard that I've reviewed correctly multiple times
    And the flashcard has 3 repetitions and is scheduled for review in 15 days
    When I review the flashcard and rate my performance as "poor" (quality 1)
    Then the flashcard's repetition count should reset to 0
    And the flashcard should be scheduled for review in 1 day
    And my ease factor should decrease

  Scenario: Getting cards that are due for review
    Given I have several flashcards with different review schedules
    And some flashcards are due for review today
    When I request cards that are due for review
    Then I should receive only the cards that are currently due
    And the cards should be ordered by their review priority

  Scenario: Getting due cards filtered by deck
    Given I have flashcards in "Math" and "History" decks
    And cards from both decks are due for review
    When I request due cards filtered by "Math" deck only
    Then I should receive only due cards from the "Math" deck
    And cards from other decks should not be included

  Scenario: Reviewing with invalid quality score
    Given I have a flashcard ready for review
    When I attempt to review the flashcard with an invalid quality score of 6
    Then the system should reject the review
    And I should receive a validation error message
    And the flashcard should remain unchanged

  Scenario: Attempting to review a non-existent flashcard
    Given I try to review a flashcard that doesn't exist
    When I submit the review with any quality score
    Then I should receive an error message
    And the system should indicate the flashcard was not found

  Scenario: Ease factor minimum boundary
    Given I have a flashcard with the minimum ease factor of 1.3
    When I review the flashcard with the worst possible performance (quality 0)
    Then the ease factor should not decrease below the minimum threshold
    And the flashcard should still be rescheduled appropriately
