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


def load_product_list(context, name):
    """Refresh the product list and wait for a matching product row."""
    wait = WebDriverWait(context.browser, 10)
    wait_for_products(context)

    wait.until(
        EC.element_to_be_clickable((By.ID, "list-all"))
    ).click()

    def find_row(driver):
        for row in driver.find_elements(By.CSS_SELECTOR, "#products tr"):
            if name in row.text:
                return row
        return False

    return wait.until(find_row)


@when('I select the product "{name}"')
def step_select_product(context, name):
    """Read a product using its Read button."""
    row = load_product_list(context, name)

    button = row.find_element(
        By.XPATH, './/button[normalize-space()="Read"]'
    )
    WebDriverWait(context.browser, 10).until(
        EC.element_to_be_clickable(button)
    ).click()


@when('I update the product "{old_name}" name to "{new_name}"')
def step_update_product(context, old_name, new_name):
    """Update a product using the admin form."""
    wait = WebDriverWait(context.browser, 10)
    row = load_product_list(context, old_name)

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
            new_name in row.text
            for row in driver.find_elements(By.CSS_SELECTOR, "#products tr")
        )
    )


@when('I delete the product "{name}"')
def step_delete_product(context, name):
    """Delete a product using its Delete button."""
    wait = WebDriverWait(context.browser, 10)
    row = load_product_list(context, name)

    delete_button = row.find_element(
        By.XPATH, './/button[normalize-space()="Delete"]'
    )
    wait.until(EC.element_to_be_clickable(delete_button)).click()

    wait.until(
        lambda driver
