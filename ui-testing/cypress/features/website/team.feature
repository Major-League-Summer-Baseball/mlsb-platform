Feature: The homepage for a team

    Features related to a team homepage such as join league requests

Background:
    Given some team exists

Scenario: Anonymous users can view a team homepage
    When I navigate to the team page
    Then I see the team page

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

