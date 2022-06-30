Feature: The homepage for a team

    Features related to a team homepage such as join league requests

Background:
    Given some team exists

Scenario: Anonymous users can view a team homepage
    When I navigate to the team page
    Then I see the team page
     And I can not make a request to join

Scenario: Captain can respond to requests to join their team 
    Given I am the Captain
      And someone has requested to join the team
     When I navigate to the team page
      And accept the request
     Then a player is added to the league
      And the player is part of the team

Scenario: Players can request to join a team
    Given I am logged in as a player
     When I navigate to the team page
     Then I can make a request to join

Scenario: Captain can add a player to their team
    Given there is some player
      And I am the Captain
     When I navigate to the team page
      And I add the player
     Then the player is part of the team

Scenario: Captain can remove a player from their team
    Given there is a player on my team
      And I am the Captain
     When I navigate to the team page
      And I remove the player
     Then the player is not part of the team

