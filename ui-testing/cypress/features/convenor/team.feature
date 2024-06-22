Feature: Convenor able to manage teams and their rosterssponsors

    Feature able to:
        Create a team
        Edit a team
        Manager team roster

Background:
    Given I am logged in as a convenor

Scenario: Able to add a new team
    Given a sponsor exists
      And a league exists
     When I navigate to the "teams" page
      And choose new team
      And I fill out the team details
     Then I see team was created

Scenario: Able to update a team
    Given a sponsor exists
      And a league exists
      And a team exists
     When I navigate to the "teams" page
      And choose the team
      And I update the team details
     Then I see team was updated

Scenario: Able to add a player to a team
    Given a sponsor exists
      And a league exists
      And a team exists
      And a player exists
     When I navigate to the "teams" page
      And choose the team
      And I add the player to team
     Then I see them on the team

Scenario: Able to add a player to a team
    Given a sponsor exists
      And a league exists
      And a team exists
      And a player exists
      And player is on the team
     When I navigate to the "teams" page
      And choose the team
      And I remove the player to team
     Then I dont see them on the team

Scenario: Able to select player as captain
    Given a sponsor exists
      And a league exists
      And a team exists
      And a player exists
     When I navigate to the "teams" page
      And choose the team
      And I add the player to team
      And I make them the captain
     Then I see they the captain

Scenario: Able to download the team template
    When I navigate to the "teams" page
     And select team template
    Then the team template is downloaded

Scenario: Able to remove a team
    Given a sponsor exists
      And a league exists
      And a team exists
     When I navigate to the "teams" page
      And choose the team
      And I remove the team
     Then I see team was removed