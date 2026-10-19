"""Selenium step definitions for Product Catalogue BDD tests."""

import time

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
    """Load products and report what the browser actually sees."""
    wait = WebDriverWait(context.browser, 10)
    wait_for_products(context)

    wait.until(
        EC.element_to_be_clickable((By.ID, "list-all"))
    ).click()

    time.sleep(1)

    rows = context.browser.find_elements(
        By.CSS_SELECTOR, "#products tr"
    )
    visible_rows = [row.text for row in rows]

    print("DEBUG page URL:", context.browser.current_url)
    print("DEBUG table rows:", visible_rows)

    for row in rows:
        if name in row.text:
            return row

    raise AssertionError(
        f"Product '{name}' was not found. Visible rows: {visible_rows}"
    )


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
    row = load_product_list(context, name)

    delete_button = row.find_element(
        By.XPATH, './/button[normalize-space()="Delete"]'
    )
    wait.until(EC.element_to_be_clickable(delete_button)).click()

    wait.until(
        lambda driver: all(
            name not in product_row.text
            for product_row in driver.find_elements(
                By.CSS_SELECTOR, "#products tr"
            )
        )
    )


@when("I list all products")
def step_list_all_products(context):
    """Display every product."""
    wait = WebDriverWait(context.browser, 10)
    wait.until(
        EC.element_to_be_clickable((By.ID, "list-all"))
    ).click()
    wait_for_products(context)


@when('I search products by name "{name}"')
def step_search_by_name(context, name):
    """Filter products by name."""
    wait = WebDriverWait(context.browser, 10)
    search = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '#search-form input[name="name"]')
        )
    )
    search.clear()
    search.send_keys(name)

    context.browser.find_element(
        By.CSS_SELECTOR, '#search-form button[type="submit"]'
    ).click()

    wait.until(
        lambda driver: any(
            name in row.text
            for row in driver.find_elements(By.CSS_SELECTOR, "#products tr")
        )
    )


@when('I search products by category "{category}"')
def step_search_by_category(context, category):
    """Filter products by category."""
    wait = WebDriverWait(context.browser, 10)
    category_select = Select(
        wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, '#search-form select[name="category"]')
            )
        )
    )
    category_select.select_by_value(category)

    context.browser.find_element(
        By.CSS_SELECTOR, '#search-form button[type="submit"]'
    ).click()

    wait.until(
        lambda driver: any(
            category in row.text
            for row in driver.find_elements(By.CSS_SELECTOR, "#products tr")
        )
    )


@when('I search products by availability "{availability}"')
def step_search_by_availability(context, availability):
    """Filter products by availability."""
    wait = WebDriverWait(context.browser, 10)
    available_select = Select(
        wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, '#search-form select[name="available"]')
            )
        )
    )
    available_select.select_by_value(availability)

    context.browser.find_element(
        By.CSS_SELECTOR, '#search-form button[type="submit"]'
    ).click()

    expected_name = "Apple" if availability == "false" else "Hammer"
    wait.until(
        lambda driver: any(
            expected_name in row.text
            for row in driver.find_elements(By.CSS_SELECTOR, "#products tr")
        )
    )


@then('I should see "{text}"')
def step_should_see(context, text):
    """Verify the expected text appears in the page."""
    WebDriverWait(context.browser, 10).until(
        lambda driver: text in driver.find_element(By.TAG_NAME, "body").text
    )


@then('I should not see "{text}"')
def step_should_not_see(context, text):
    """Verify the text is absent from the product rows."""
    WebDriverWait(context.browser, 10).until(
        lambda driver: all(
            text not in row.text
            for row in driver.find_elements(By.CSS_SELECTOR, "#products tr")
        )
    )


@then('I should see the message "{message}"')
def step_should_see_message(context, message):
    """Verify the expected status message appears."""
    WebDriverWait(context.browser, 10).until(
        lambda driver: message in driver.find_element(By.ID, "message").text
    )
