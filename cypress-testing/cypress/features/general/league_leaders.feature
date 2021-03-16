Feature: The page for league leaders

    Feature for the various league leaders.

Scenario: Current Season leader page
    When I navigate to the league leaders page
    Then there is a descending ordered list of players for homeruns
     And there is a descending ordered list of players for singles

Scenario: All-time leader page
    When I navigate to the all-time leaders page
    Then there is a descending ordered list of players for all-time homeruns
     And there is a descending ordered list of players for all-time singles