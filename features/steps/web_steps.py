
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
    wait_for_products(context)
    rows = context.browser.find_elements(By.CSS_SELECTOR, "#products tr")

    for row in rows:
        if name in row.text:
            row.find_element(By.XPATH, './/button[normalize-space()="Read"]').click()
            return

    raise AssertionError(f"Product '{name}' was not found")


@when('I update the product "{old_name}" name to "{new_name}"')
def step_update_product(context, old_name, new_name):
    """Update a product using the admin form."""
    wait_for_products(context)
    rows = context.browser.find_elements(By.CSS_SELECTOR, "#products tr")

    for row in rows:
        if old_name in row.text:
            row.find_element(By.XPATH, './/button[normalize-space()="Edit"]').click()
            break
    else:
        raise AssertionError(f"Product '{old_name}' was not found")

    name_input = context.browser.find_element(
        By.CSS_SELECTOR, '#product-form input[name="name"]'
    )
    name_input.clear()
    name_input.send_keys(new_name)
    context.browser.find_element(
        By.CSS_SELECTOR, '#product-form button[type="submit"]'
    ).click()

    WebDriverWait(context.browser, 10).until(
        lambda driver: new_name in driver.find_element(By.ID, "products").text
    )


@when('I delete the product "{name}"')
def step_delete_product(context, name):
    """Delete a product using its Delete button."""
    wait_for_products(context)
    rows = context.browser.find_elements(By.CSS_SELECTOR, "#products tr")

    for row in rows:
        if name in row.text:
            row.find_element(
                By.XPATH, './/button[normalize-space()="Delete"]'
            ).click()
            WebDriverWait(context.browser, 10).until(
                lambda driver: name not in driver.find_element(
                    By.ID, "products"
                ).text
            )
            return

    raise AssertionError(f"Product '{name}' was not found")


@when("I list all products")
def step_list_all_products(context):
    """Display every product."""
    context.browser.find_element(By.ID, "list-all").click()
    wait_for_products(context)


@when('I search products by name "{name}"')
def step_search_by_name(context, name):
    """Filter products by name."""
    search = context.browser.find_element(
        By.CSS_SELECTOR, '#search-form input[name="name"]'
    )
    search.clear()
    search.send_keys(name)
    context.browser.find_element(
        By.CSS_SELECTOR, '#search-form button[type="submit"]'
    ).click()


@when('I search products by category "{category}"')
def step_search_by_category(context, category):
    """Filter products by category."""
    select = Select(context.browser.find_element(
        By.CSS_SELECTOR, '#search-form select[name="category"]'
    ))
    select.select_by_value(category)
    context.browser.find_element(
        By.CSS_SELECTOR, '#search-form button[type="submit"]'
    ).click()


@when('I search products by availability "{available}"')
def step_search_by_availability(context, available):
    """Filter products by availability."""
    select = Select(context.browser.find_element(
        By.CSS_SELECTOR, '#search-form select[name="available"]'
    ))
    select.select_by_value(available.lower())
    context.browser.find_element(
        By.CSS_SELECTOR, '#search-form button[type="submit"]'
    ).click()


@then('I should see "{text}"')
def step_should_see(context, text):
    """Verify text appears in the page."""
    WebDriverWait(context.browser, 10).until(
        lambda driver: text in driver.find_element(
            By.TAG_NAME, "body"
        ).text
    )


@then('I should not see "{text}"')
def step_should_not_see(context, text):
    """Verify text is absent from the product table."""
    WebDriverWait(context.browser, 10).until(
        lambda driver: all(
            text not in row.text
            for row in driver.find_elements(By.CSS_SELECTOR, "#products tr")
        )
    )
