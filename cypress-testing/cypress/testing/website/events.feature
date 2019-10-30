Feature: The league events
    Background:
        Given I navigate to the events page

    Scenario Outline: Clicking the various events
        When viewing the event "<eventName>"
        Then I see details relating to "<eventDescription>"

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
