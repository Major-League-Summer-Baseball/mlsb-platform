Feature: The league schedule

	Background:
		Given I navigate to the "schedule" page

	Scenario: Ensure some games are displayed
		Then I see a table cell containing "WP1"
