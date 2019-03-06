#Author: dallas.fraser.waterloo@gmail.com
#Keywords Summary : Tests thegame banner that appears at the top
@tag
Feature: Game Banner
    Background:
        Given I navigate to the "home" page

    Scenario: See a game score
        Then I see a game score in the banner