Feature: The league events

    Feature for the events of the league.


Scenario Outline: Clicking the various events
    Given I navigate to the events page
    When viewing the event "<eventName>"
    Then I see details relating to "<eventDescription>"

Examples: Events
| eventName             | eventDescription  |
| Mystery Bus           | school buses      |
| Jays Game             | boys of summer    |
| Beerlympics           | various countries |
| Rafting               | rafting           |
| Grand Bender          | All Star          |
| Summerween            | Halloween         |


Scenario: Able to sign up for event when signed in
    Given I am logged in as a player
      And I navigate to the events page
    When viewing the event "MLSB Alumni"
     And I can sign up
    Then I see details relating to "legends are born"
     And I see I am registered

