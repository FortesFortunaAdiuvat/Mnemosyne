Feature: Card Management
  As a learner
  I want to manage my flashcards
  So that I can organize my study materials effectively

  Background:
    Given the Mnemosyne learning system is running
    And I have access to the card management API

  Scenario: Creating a new flashcard
    Given I want to learn about "Geography"
    When I create a flashcard with question "What is the capital of France?" and answer "Paris"
    Then the flashcard should be saved successfully
    And the flashcard should be assigned to the "Geography" deck
    And the flashcard should be immediately available for review

  Scenario: Creating a flashcard without specifying a deck
    Given I want to create a basic flashcard
    When I create a flashcard with question "2+2=?" and answer "4" without specifying a deck
    Then the flashcard should be saved successfully
    And the flashcard should be assigned to the "default" deck

  Scenario: Viewing my flashcard collection
    Given I have created several flashcards in different decks
    When I request to view my flashcard collection
    Then I should see all my flashcards
    And the results should be paginated for easy browsing
    And I should see the total count of my flashcards

  Scenario: Filtering flashcards by deck
    Given I have flashcards in "Math" and "Science" decks
    When I filter my flashcards to show only "Math" deck
    Then I should see only flashcards from the "Math" deck
    And flashcards from other decks should not be shown

  Scenario: Updating a flashcard
    Given I have a flashcard with question "What is 2+2?" and answer "4"
    When I update the question to "What is 3+3?" and answer to "6"
    Then the flashcard should be updated successfully
    And the new content should be saved

  Scenario: Deleting a flashcard
    Given I have a flashcard I no longer need
    When I delete the flashcard
    Then the flashcard should be removed from my collection
    And it should no longer appear in my flashcard list

  Scenario: Attempting to update a non-existent flashcard
    Given I try to update a flashcard that doesn't exist
    When I submit the update request
    Then I should receive an error message
    And the system should indicate the flashcard was not found

  Scenario: Attempting to delete a non-existent flashcard
    Given I try to delete a flashcard that doesn't exist
    When I submit the delete request
    Then I should receive an error message
    And the system should indicate the flashcard was not found
