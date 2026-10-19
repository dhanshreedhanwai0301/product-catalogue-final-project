
"""Unit tests for the Product model."""

import unittest

from service.models import db, Product, Category
from tests.factories import ProductFactory


class TestProduct(unittest.TestCase):
    """Test cases for Product model operations."""

    def setUp(self):
        """Create a fresh database for each test."""
        self.app = __import__("flask").Flask(__name__)
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db.init_app(self.app)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """Remove the database after each test."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_read_a_product(self):
        """It should read a product."""
        product = ProductFactory()
        db.session.add(product)
        db.session.commit()

        found = db.session.get(Product, product.id)
        self.assertIsNotNone(found)
        self.assertEqual(found.name, product.name)

    def test_update_a_product(self):
        """It should update a product."""
        product = ProductFactory()
        db.session.add(product)
        db.session.commit()

        product.name = "Updated Product"
        db.session.commit()

        found = db.session.get(Product, product.id)
        self.assertEqual(found.name, "Updated Product")

    def test_delete_a_product(self):
        """It should delete a product."""
        product = ProductFactory()
        db.session.add(product)
        db.session.commit()
        product_id = product.id

        db.session.delete(product)
        db.session.commit()

        self.assertIsNone(db.session.get(Product, product_id))

    def test_list_all_products(self):
        """It should list all products."""
        db.session.add_all(ProductFactory.create_batch(3))
        db.session.commit()

        products = Product.query.all()
        self.assertEqual(len(products), 3)

    def test_find_by_name(self):
        """It should find products by name."""
        product = ProductFactory(name="Hammer")
        db.session.add(product)
        db.session.commit()

        found = Product.query.filter_by(name="Hammer").all()
        self.assertEqual(len(found), 1)

    def test_find_by_category(self):
        """It should find products by category."""
        product = ProductFactory(category=Category.TOOLS)
        db.session.add(product)
        db.session.commit()

        found = Product.query.filter_by(category=Category.TOOLS).all()
        self.assertEqual(len(found), 1)

    def test_find_by_availability(self):
        """It should find products by availability."""
        product = ProductFactory(available=True)
        db.session.add(product)
        db.session.commit()

        found = Product.query.filter_by(available=True).all()
        self.assertEqual(len(found), 1)


if __name__ == "__main__":
    unittest.main()
