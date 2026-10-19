
"""Load background product data for Behave scenarios."""

from behave import given

from service.models import db, Product, Category


@given("the following products")
def step_impl(context):
    """Load the products provided in the feature file."""
    with context.app.app_context():
        db.session.query(Product).delete()

        for row in context.table:
            category_name = row["category"].upper()
            category = Category[category_name]

            product = Product(
                name=row["name"],
                description=row.get("description", ""),
                price=float(row.get("price", "0")),
                available=row.get("available", "true").lower() == "true",
                category=category,
            )
            db.session.add(product)

        db.session.commit()
