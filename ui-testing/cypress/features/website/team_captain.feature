Feature: The homepage for a team

    Features related to a team homepage such as join league requests

Background:
    Given some team exists
      And there is some player
      And I am the Captain

Scenario: Captain can add players that have requested to join
    Given someone has requested to join the team
     When I navigate to the team page
      And accept the request
     Then a player is added to the league
      And the player is part of the team

Scenario: Captain can reject players that have requested to join
    Given someone has requested to join the team
     When I navigate to the team page
      And decline the request
     Then a player is not added to the league

Scenario: Captain can find existing player and add them to their team
     When I navigate to the team page
      And I search for the player
      And I add them to my team
     Then a player is added to the league
      And the player is part of the team

Scenario: Captain can create new player and add them to their team
     When I navigate to the team page
      And I search for the nonexistent player
      And I add a new player
     Then a player is added to the league
      And the player is part of the team

Scenario: Captain can remove a player from their team
    Given there is a player on my team
      And I am the Captain
     When I navigate to the team page
      And I remove the player
     Then the player is not part of the team