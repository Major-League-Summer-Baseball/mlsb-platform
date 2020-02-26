#Author: dallas.fraser.waterloo@gmail.com
#Keywords Summary : Test the sponsor banner at the top

Feature: The league schedule

    Scenario: Ensure the table is properly displayed
       Given I am on the the schedule page
        Then I see the schedule for the league
