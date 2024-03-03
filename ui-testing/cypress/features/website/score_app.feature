Feature: The captain score app

    Tests the score app for a captain

    Scenario: Score cannot be negative
        Given I am captain of a team
          And submitting a score for a game
         When score is -1
         Then I am unable to submit score
          And see prompt about "negative score"

    Scenario: Homeruns cannot be greater than score
        Given I am captain of a team
          And submitting a score for a game
         When score is 0
          And I got a homerun
         Then I am unable to submit score
          And see prompt about "homerun"

    Scenario: Able to submit a score
        Given I am captain of a team
          And submitting a score for a game
         When score is 5
          And I got a homerun
          And I am able to submit
         Then the score is submitted
          And I no longer see the game