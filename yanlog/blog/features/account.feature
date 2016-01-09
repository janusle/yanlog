Feature: User login and logout

    Scenario: User login
        Given I access the url 'accounts/login/'
        Then I see login page
