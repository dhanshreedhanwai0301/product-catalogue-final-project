
Feature: Manage products in the catalogue
  As an administrator
  I want to manage products
  So that the catalogue stays up to date

  Background:
    Given the following products
      | name   | description     | price | available | category |
      | Hammer | Steel hammer    | 10.00 | true      | TOOLS    |
      | Shirt  | Cotton shirt    | 20.00 | true      | CLOTHS   |
      | Apple  | Fresh apple     | 2.00  | false     | FOOD     |

  Scenario: Read a product
    When I select the product "Hammer"
    Then I should see "Hammer"

  Scenario: Update a product
    When I update the product "Hammer" name to "Large Hammer"
    Then I should see "Large Hammer"

  Scenario: Delete a product
    When I delete the product "Hammer"
    Then I should not see "Hammer"

  Scenario: List all products
    When I list all products
    Then I should see "Hammer"
    And I should see "Shirt"
    And I should see "Apple"

  Scenario: Search products by name
    When I search products by name "Hammer"
    Then I should see "Hammer"
    And I should not see "Shirt"

  Scenario: Search products by category
    When I search products by category "FOOD"
    Then I should see "Apple"
    And I should not see "Hammer"

  Scenario: Search products by availability
    When I search products by availability "false"
    Then I should see "Apple"
    And I should not see "Hammer"
