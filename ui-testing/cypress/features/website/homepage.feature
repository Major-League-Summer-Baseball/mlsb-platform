Feature: The homepage and the game banner at the top

    The homepage of the league.

Scenario: The game banner contains recent and upcoming games
    When I navigate to the home page
    Then there is a list of recent game scores

Scenario: A list of active sponsors are displayed
    When I navigate to the home page
    Then there is a list of sponsors
    And I can navigate through the list of sponsors

Scenario: Summaries of news items are displayed
    When I navigate to "2016" home page
    Then there is a list of news items

Scenario: Able to view a news item
    When I navigate to "2016" home page
        And I click on "Launch" news item
    Then I see details about website launch
