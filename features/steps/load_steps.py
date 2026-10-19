
"""Load background product data for Behave scenarios."""

from behave import given

from service.models import db, Product, Category


@given("the following products")
def step_load_products(context):
    """Load products from the feature file's background table."""
    with context.app.app_context():
        db.session.query(Product).delete()

        for row in context.table:
            category_name = row["category"].strip().upper()

            if category_name not in Category.__members__:
                raise AssertionError(
                    f"Unknown product category: {category_name}"
                )

            product = Product(
                name=row["name"],
                description=row["description"],
                price=float(row["price"]),
                available=row["available"].strip().lower() == "true",
                category=Category[category_name],
            )
            db.session.add(product)

        db.session.commit()
