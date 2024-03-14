Feature: The homepage for a team

    Features related to a team homepage such as join league requests

Background:
    Given some team exists

Scenario: Anonymous users can view a team homepage
    When I navigate to the team page
     And I see the team page
     And I can make a request to join
     And I fill out my details
    Then I see my request is pending

Scenario: Players can request to join a team
    Given I am logged in as a player
     When I navigate to the team page
      And I see the team page
      And I can make a request to join
     Then I see my request is pending
