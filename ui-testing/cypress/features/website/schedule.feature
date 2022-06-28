Feature: The league schedule

    Feature for the league schedule that lets people know
    when their games are.

Scenario: Ensure the table is properly displayed
    Given I am on the the schedule page
    Then I see the schedule for the league
