Feature: The fields and rules

    Feature for the fields and rules of the league.

Background:
    Given I navigate to the rules and fields page

Scenario: Checking the rules tab
    When I click on "Rules" tab
    Then I see information about the rules

Scenario: Check the fields tab
    When I click on "Fields" tab
    Then I see information about the fields
