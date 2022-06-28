@login
Feature: Logging into Admin Panel

Scenario: Login using the UI
    When I am logged in as an admin
    Then I am logged in

Scenario: Failing to log into MLSB using invalid credentials
    When I navigate to the login page
     And I enter invalid credentials
    Then I see a login error message
