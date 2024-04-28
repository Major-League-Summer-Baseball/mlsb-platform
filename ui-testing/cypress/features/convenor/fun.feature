Feature: Convenor able to manage fun counts

    Feature for a convenor able to manage fun counts

Background:
    Given I am logged in as a convenor

Scenario: Able to add a fun
    When I navigate to the "fun" page
     And I fill out the fun details
     And I submit fun
    Then I see fun was created

Scenario: Able to edit a fun
    Given a fun exists
     When I navigate to the "fun" page
      And I update the fun details
     Then I see fun was updated
