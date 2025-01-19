Feature: Convenor able to manage sponsors

    Feature for a convenor able to manage sponsors

Background:
    Given I am logged in as a convenor

Scenario: Able to add a new sponsor
    When I navigate to the "sponsors" page
     And I fill out the sponsor details
     And I submit sponsor
    Then I see sponsor was created

Scenario: Able to edit a sponsor
    Given a sponsor exists
    When I navigate to the "sponsors" page
     And I update the sponsor details
     And I click update
    Then I see sponsor was updated

Scenario: Able to hide a sponsor
    Given a sponsor exists
     When I navigate to the "sponsors" page
      And I hide the sponsor
     Then sponsor is no longer visible

Scenario: Able to add a sponsor logo
    Given a sponsor exists
     When I navigate to the "sponsors" page
      And I upload a new logo
      And I click update
     Then I see sponsor was updated
      And I see the logo
