Feature: The batting app for captains to keep track of stats.

    Tests the batting app. The app will filter out the team roster to ensure there is just one guy and one girl. This it to make testing easier.

Background:
     Given I am captain of a team
       And my team had a game
       And using the batting app for the game
    
# BATS AND OUTS
Scenario Outline: Batting hits allow runners to advance to their base
    When the batter hits a "<batName>"
    Then the batter advances to "<base>"

Examples: Bats
| batName | base       |
| E       | first |
| S       | first |
| D       | second|
| T       | third |

Scenario Outline: Batter gets out and outs are increase
    When the batter gets out by "<out>"
    Then there is 1 out

Examples: Outs
| out |
| K   |
| GO  |
| FO  |
| Auto|

# SPECIAL HITS
Scenario: Player hits a homerun
    When the bases are loaded
     And the batter hits a "HR"
    Then the score is 4

Scenario: Players hits a sacrifice-fly
    When the bases are loaded
     And the batter hits a "SF"
    Then the score is 1
     And there is 1 out

Scenario: Only eligble players can get Sapporo Singles
    When the batter is eligble
     And the batter hits a "SS"
    Then the batter advances to "first"

Scenario: Non-eligble players do not see Sapporo Singles
    When the batter is not eligble
    Then they cannot hit a "SS"

# GAME LOGIC
Scenario: Three outs end the inning
    When the batter gets out by "K"
     And the batter gets out by "K"
     And the batter gets out by "K"
    Then there are 0 outs
     And it is the 2 inning

# UNDO FEATURE
Scenario: Able to undo a hit
    When the batter hits a "hr"
     And the score is 1
     And I undo the hit
    Then the score is 0

# LINEUP MANAGEMENT
Scenario: Able to remove player from the lineup
    When I remove a player from the lineup
    Then they are not in the lineup

Scenario: Able to move player to bottom of the lineup
    When I move a player to the bottom of the lineup
    Then they are on the bottom of the lineup

Scenario: Able to move player to bottom of the lineup
    When I move a plyer to the top of the lineup
    Then they are at the top of the lineup

# GAME CONTROLS - SUBMISSION AND RESTART
Scenario: Able to restart a game
    When the batter hits a "HR"
     And the score is 1
     And restart the game
    Then the score is 0

Scenario: Able to submit a game
    When the batter hits a "HR"
     And submit the game
    Then score submission is accepted
