
"""Selenium step definitions for product catalogue BDD tests."""

from behave import when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_browser(context):
    """Return the Selenium browser configured by the environment."""
    return context.browser


def find_product_row(context, name):
    """Find a product row containing the given product name."""
    browser = get_browser(context)
    rows = browser.find_elements(By.CSS_SELECTOR, "tr")
    for row in rows:
        if name in row.text:
            return row
    return None


@when('I select the product "{name}"')
def step_select_product(context, name):
    """Open the selected product."""
    browser = get_browser(context)
    row = find_product_row(context, name)
    assert row is not None, f"Product '{name}' was not found"
    row.click()


@when('I update the product "{old_name}" name to "{new_name}"')
def step_update_product(context, old_name, new_name):
    """Update a product name through the UI."""
    browser = get_browser(context)
    row = find_product_row(context, old_name)
    assert row is not None, f"Product '{old_name}' was not found"

    edit_button = row.find_element(
        By.XPATH,
        './/button[contains(translate(text(), "EDIT", "edit"), "edit")]'
    )
    edit_button.click()

    name_input = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'input[name="name"]')
        )
    )
    name_input.clear()
    name_input.send_keys(new_name)

    save_button = browser.find_element(
        By.XPATH,
        '//button[contains(translate(text(), "SAVE", "save"), "save")]'
    )
    save_button.click()


@when('I delete the product "{name}"')
def step_delete_product(context, name):
    """Delete a product through the UI."""
    browser = get_browser(context)
    row = find_product_row(context, name)
    assert row is not None, f"Product '{name}' was not found"

    delete_button = row.find_element(
        By.XPATH,
        './/button[contains(translate(text(), "DELETE", "delete"), "delete")]'
    )
    delete_button.click()


@when("I list all products")
def step_list_all_products(context):
    """Display all products."""
    browser = get_browser(context)
    browser.find_element(
        By.XPATH,
        '//button[contains(translate(text(), "ALL", "all"), "all")]'
    ).click()


@when('I search products by name "{name}"')
def step_search_by_name(context, name):
    """Search products by name."""
    browser = get_browser(context)
    search_input = browser.find_element(
        By.CSS_SELECTOR, 'input[name="name"]'
    )
    search_input.clear()
    search_input.send_keys(name)
    search_input.submit()


@when('I search products by category "{category}"')
def step_search_by_category(context, category):
    """Filter products by category."""
    browser = get_browser(context)
    category_input = browser.find_element(
        By.CSS_SELECTOR, 'select[name="category"]'
    )
    from selenium.webdriver.support.ui import Select
    Select(category_input).select_by_visible_text(category)


@when('I search products by availability "{available}"')
def step_search_by_availability(context, available):
    """Filter products by availability."""
    browser = get_browser(context)
    availability_input = browser.find_element(
        By.CSS_SELECTOR, 'select[name="available"]'
    )
    from selenium.webdriver.support.ui import Select
    Select(availability_input).select_by_visible_text(available)


@then('I should see "{text}"')
def step_should_see(context, text):
    """Verify that text appears on the page."""
    browser = get_browser(context)
    WebDriverWait(browser, 10).until(
        lambda driver: text in driver.find_element(
            By.TAG_NAME, "body"
        ).text
    )


@then('I should not see "{text}"')
def step_should_not_see(context, text):
    """Verify that text does not appear on the page."""
    browser = get_browser(context)
    WebDriverWait(browser, 10).until(
        lambda driver: text not in driver.find_element(
            By.TAG_NAME, "body"
        ).text
    )
