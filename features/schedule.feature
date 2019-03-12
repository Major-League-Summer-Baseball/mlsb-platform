#Author: dallas.fraser.waterloo@gmail.com
#Keywords Summary : Test the sponsor banner at the top

Feature: The league schedule

    Background:
        Given I navigate to the "schedule" page

    Scenario: Ensure some games are displayed
        Then I see a table cell containing "WP1"

    Scenario: Ensure table sorted by date and on today
        Then I see a table cell containing today's date