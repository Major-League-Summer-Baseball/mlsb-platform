#Author: dallas.fraser.waterloo@gmail.com
#Keywords Summary : Test the league events

Feature: The league events
    Background:
        Given I navigate to the "events" page

    Scenario Outline: Clicking the various events
        When I click on "<eventName>" event button
        Then I see a event paragraph containing "<eventDescription>"

    Examples: Events
    | eventName             | eventDescription  |
    | Mystery Bus           | school buses      |
    | Blue Jays Game        | boys of summer    |
    | Beerfest              | various countries |
    | Rafting               | rafting           |
    | Beerwell Classic      | All Star          |
    | Hitting for the Cycle | pub crawl         |
    | Summerween            | Halloween         |
    | ESPY Awards           | end of the summer |
