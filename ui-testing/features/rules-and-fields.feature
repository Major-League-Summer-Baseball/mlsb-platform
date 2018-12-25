Feature: The fields and rules
	Background:
		Given I navigate to the "fieldsrules" page

	Scenario: Checking the two different pages
		When I click on "Rules" tab
		Then I see a paragraph containing "official MLSB Rules"
		When I click on "Fields" tab
		Then I see a paragraph containing "games take place"
