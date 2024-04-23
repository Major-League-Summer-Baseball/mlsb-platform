Feature: Convenor able to manage league events

    Feature for a convenor able to create new events, hide events and add dates

Background:
    Given I am logged in as a convenor

# Skipping for now since manipulate ckeditor
@skip
Scenario: Able to add a league event
    When I navigate to the "events" page

     And I fill out the league events details
     And I submit league event
    Then I see "league event" was "created"

Scenario: Able to edit a league event
    Given a league event exists
     When I navigate to the "events" page
      And I update the league event details
     Then I see "league event" was "updated"

Scenario: Able to hide a league event
    Given a league event exists
     When I navigate to the "events" page
      And I hide the league event
     Then I see league event is hidden

Scenario: Able to add new date
    Given a league event exists
     When I navigate to the "events" page
      And see dates for the league event
      And I enter a new date
     Then I see "League event date" was "created"
