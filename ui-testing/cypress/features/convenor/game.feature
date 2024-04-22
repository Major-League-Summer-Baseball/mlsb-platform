Feature: Convenor able to manage games

    Feature able to add and update games

Background:
    Given I am logged in as a convenor

Scenario: Able to add a new game
    Given two team exists
      And a division exists
     When I navigate to the "games" page
      And choose new game
      And I fill out the game details
     Then I see game was created

Scenario: Able to add a update game
    Given a game exists
     When I navigate to the "games" page
      And choose the game
      And I update the game details
     Then I see game was updated

Scenario: Able to download the game template
    When I navigate to the "games" page
     And select game template
    Then the game templated is downloaded
