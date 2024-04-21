Feature: Convenor able to manage sponsors

    Feature for a convenor able to manage sponsors

Background:
    Given I am logged in as a convenor
     And I navigate to the "sponsors" page

@focus
Scenario: Able to add a new sponsor
    When I fill out the sponsor details
     And I submit sponsor
    Then I see sponsor was created

Scenario: Able to edit a sponsor
    Given a sponsor exists
    When I update the sponsor details
     And I click update
    Then I see sponsor was updated

Scenario: Able to hide a sponsor
    Given a sponsor exists
     When I hide the sponsor
     Then sponsor is no longer visible

