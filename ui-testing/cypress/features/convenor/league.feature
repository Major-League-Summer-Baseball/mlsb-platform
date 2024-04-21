Feature: Convenor able to manage leagues and division

    Feature for a convenor able to manage leagues and divisions

Background:
    Given I am logged in as a convenor

Scenario: Able to add a new league
    When I navigate to the "leagues" page
     And I fill out the league details
     And I submit league
    Then I see league was created

Scenario: Able to update a league
    Given a league exists
     When I navigate to the "leagues" page
      And I update the league details
     Then I see league was updated

Scenario: Able to add a new division
    When I navigate to the "leagues" page
     And I fill out the division details
     And I submit division
    Then I see division was created

Scenario: Able to update a division
    Given a division exists
     When I navigate to the "leagues" page
      And I update the division details
     Then I see division was updated
