#Author: dallas.fraser.waterloo@gmail.com
#Keywords Summary : Test the fields and rules

Feature: The fields and rules
    Background:
        Given I navigate to the "fieldsrules" page

    Scenario: Checking the rules tab
        When I click on "Rules" tab
        Then I see a paragraph containing "official MLSB Rules"

    Scenario: Check the fields tab
        When I click on "Fields" tab
        Then I see a paragraph containing "games take place"
