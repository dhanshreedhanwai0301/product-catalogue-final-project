Feature: Manage products in the catalogue
  As an administrator
  I want to manage products
  So that the catalogue stays up to date

  Background:
    Given the following products
      | name   | description  | price | available | category |
      | Mallet | Wooden mallet | 10.00 | true      | TOOLS    |
      | Shirt  | Cotton shirt | 20.00 | true      | CLOTHS   |
      | Apple  | Fresh apple  | 2.00  | false     | FOOD     |

  Scenario: Read a product
    When I select the product "Mallet"
    Then I should see "Mallet"

  Scenario: Update a product
    When I update the product "Mallet" name to "Large Mallet"
    Then I should see "Large Mallet"

  Scenario: Delete a product
    When I delete the product "Mallet"
    Then I should not see "Mallet"

  Scenario: List all products
    When I list all products
    Then I should see "Mallet"
    And I should see "Shirt"
    And I should see "Apple"

  Scenario: Search products by name
    When I search products by name "Mallet"
    Then I should see "Mallet"
    And I should not see "Shirt"

  Scenario: Search products by category
    When I search products by category "FOOD"
    Then I should see "Apple"
    And I should not see "Mallet"

  Scenario: Search products by availability
    When I search products by availability "false"
    Then I should see "Apple"
    And I should not see "Mallet"
