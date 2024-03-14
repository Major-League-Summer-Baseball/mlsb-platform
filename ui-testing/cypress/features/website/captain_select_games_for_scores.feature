Feature: As a captain I can select score or batting app for submitting scores

    Tests the score app for a captain

    Scenario: Past Games without scores are listed on the page and can use score app
        Given I am captain of a team
          And my team had a game
         When I view the list of Games
         Then the game is elible for submission
          And I can begin to submit my score

    Scenario: Past Games without scores are listed on the page and can use batting app
        Given I am captain of a team
          And my team had a game
         When I view the list of Games
         Then the game is elible for submission
          And I can start the batting app

    Scenario: Submitted games are eligible for resubmission
        Given I am captain of a team
          And my team had a game
          And my score has been submitted
         When I view the list of Games
          And I click resubmit
         Then the game is elible for submission