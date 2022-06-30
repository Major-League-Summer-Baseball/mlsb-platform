Feature: The league events

    Feature for the events of the league.

Background:
    Given I navigate to the events page

Scenario Outline: Clicking the various events
    When viewing the event "<eventName>"
    Then I see details relating to "<eventDescription>"

Examples: Events
| eventName             | eventDescription  |
| Mystery Bus           | school buses      |
| Blue Jays Game        | boys of summer    |
| Beerlympics           | various countries |
| Rafting               | rafting           |
| Grand Bender          | All Star          |
| Summerween            | Halloween         |
| ESPY Awards           | end of the summer |
