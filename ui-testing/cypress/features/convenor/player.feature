Feature: Convenor able to manage players

    Feature for a convenor able to search for players,
    respond league request and add/update player

Background:
    Given I am logged in as a convenor


Scenario: Able to add a new player
    When I navigate to the "players" page
     And I click "Add Player"
     And I fill out the player details
     And I submit player
    Then I see player was created

Scenario: Able to edit a player
    Given a player exists
     When I navigate to the "players" page
      And I search for the player
      And I select the player
      And I update the player details
     Then I see player was updated

Scenario: Able to respond to league request
    Given a player has requested to join league
     When I navigate to the "players" page
      And I respond to their request
     Then I see request was accepted

@focus
Scenario: Able to merge player
    Given a players exists
     When I navigate to the "players" page
      And I search for the player
      And I select the player
      And I merge the player
     Then I see player was merged