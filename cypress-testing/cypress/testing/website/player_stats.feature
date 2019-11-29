Feature: The page for player stats
    Background:
        Given I am on the player stats page

    Scenario: Ability to get individual player information
        When I click on some player name
        Then I see their career stats

    Scenario: Ability to sort by player name
        When I sort by "name"
        Then the players are sorted "alphabetically" by "name"

    @focus
    Scenario: Ability to sort by player stats
        When I sort by "ss"
        Then the players are sorted "numerically" by "ss"

    Scenario: Filter by player name
        When I search for "a"
        Then players name contain "a"

    Scenario: Filter but with no matching results
        When I search for "does not exist 9234"
        Then no matching records were found
