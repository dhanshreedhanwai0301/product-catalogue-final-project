"""Selenium step definitions for Product Catalogue BDD tests."""

from behave import when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


def wait_for_products(context):
    """Wait until the product table is available."""
    return WebDriverWait(context.browser, 10).until(
        EC.presence_of_element_located((By.ID, "products"))
    )


@when('I select the product "{name}"')
def step_select_product(context, name):
    """Read a product using its Read button."""
    wait = WebDriverWait(context.browser, 10)
    wait_for_products(context)

    rows = context.browser.find_elements(
        By.CSS_SELECTOR, "#products tr"
    )

    for row in rows:
        if name in row.text:
            button = row.find_element(
                By.XPATH, './/button[normalize-space()="Read"]'
            )
            wait.until(EC.element_to_be_clickable(button)).click()
            return

    raise AssertionError(f"Product '{name}' was not found")


@when('I update the product "{old_name}" name to "{new_name}"')
def step_update_product(context, old_name, new_name):
    """Update a product using the admin form."""
    wait = WebDriverWait(context.browser, 10)
    wait_for_products(context)

    row_xpath = (
        f'//table[@id="products"]//tr'
        f'[.//*[contains(normalize-space(), "{old_name}")]]'
    )

    row = wait.until(
        EC.presence_of_element_located((By.XPATH, row_xpath))
    )

    edit_button = row.find_element(
        By.XPATH, './/button[normalize-space()="Edit"]'
    )
    wait.until(EC.element_to_be_clickable(edit_button)).click()

    name_input = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '#product-form input[name="name"]')
        )
    )
    name_input.clear()
    name_input.send_keys(new_name)

    save_button = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#product-form button[type="submit"]')
        )
    )
    save_button.click()

    wait.until(
        lambda driver: any(
            new_name in product_row.text
            for product_row in driver.find_elements(
                By.CSS_SELECTOR, "#products tr"
            )
        )
    )


@when('I delete the product "{name}"')
def step_delete_product(context, name):
    """Delete a product using its Delete button."""
    wait = WebDriverWait(context.browser, 10)
    wait_for_products(context)

    row_xpath = (
        f'//table[@id="products"]//tr'
        f'[.//*[contains(normalize-space(), "{name}")]]'
    )

    row = wait.until(
        EC.presence_of_element_located((By.XPATH, row_xpath))
    )

    delete_button = row.find_element(
        By.XPATH, './/button[normalize-space()="Delete"]'
    )
    wait.until(EC.element_to_be_clickable(delete_button)).click()

    wait.until(
        lambda driver: all(
            name not in product_row.text
            for product_row in driver.find_elements
