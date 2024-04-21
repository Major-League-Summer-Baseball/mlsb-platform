@skip
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
     When I navigate to the "players" page
      And choose new team
      And I fill out the team details
     Then I see team was created

Scenario: Able to update a team
    Given a sponsor exists
      And a league exists
      And a team exists
     When I navigate to the "players" page
      And choose the team
      And I update the team details
     Then I see team was updated
