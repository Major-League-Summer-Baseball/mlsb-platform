#Author: dallas.fraser.waterloo@gmail.com
#Keywords Summary : Tests the players stats table

@tag
Feature: Player Stats
    Background:
        Given I navigate to the "stats" page

    Scenario: Ensure some stats are shown
        Then I see a table cell containing "0"
        And I see a table cell containing "1"