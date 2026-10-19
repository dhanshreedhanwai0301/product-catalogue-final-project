"""Step definitions for loading products into the database."""

from behave import given

from service.models import db, Product, Category


@given("the following products")
def step_load_products(context):
    """Load products from the feature table."""
    with context.app.app_context():
        db.session.remove()
        Product.query.delete()
        db.session.commit()

        for row in context.table:
            product = Product(
                name=row["name"],
                description=row["description"],
                price=float(row["price"]),
                available=row["available"].strip().lower() == "true",
                category=Category[row["category"].strip().upper()],
            )
            db.session.add(product)

        db.session.commit()

    # Reload the page so the browser displays the newly loaded products.
    context.browser.get(context.base_url)
