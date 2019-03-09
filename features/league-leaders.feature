#Author: dallas.fraser.waterloo@gmail.com
#Keywords Summary : Tests the league leaders table
@tag
Feature: League Leaders
    Background:
        Given I navigate to the "leagueleader" page

    Scenario: I see some league leaders
        Then I see some league leaders
        And the top leaders has more than bottom
