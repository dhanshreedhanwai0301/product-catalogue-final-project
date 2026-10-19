
"""Tests for the Product Catalogue REST API."""

import unittest

from service import create_app
from service.models import db, Product, Category


class TestProductRoutes(unittest.TestCase):
    """Test product API endpoints."""

    def setUp(self):
        """Create an isolated test application and database."""
        self.app = create_app({
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        })
        self.client = self.app.test_client()

        with self.app.app_context():
            db.drop_all()
            db.create_all()

    def tearDown(self):
        """Clean up the database."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def create_product(
        self, name="Hammer", category=Category.TOOLS, available=True
    ):
        """Insert a product into the test database."""
        with self.app.app_context():
            product = Product(
                name=name,
                description="Test product",
                price=10.00,
                category=category,
                available=available,
            )
            db.session.add(product)
            db.session.commit()
            product_id = product.id
        return product_id

    def test_read_product(self):
        product_id = self.create_product()
        response = self.client.get(f"/products/{product_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["name"], "Hammer")

    def test_update_product(self):
        product_id = self.create_product()
        response = self.client.put(
            f"/products/{product_id}",
            json={"name": "Updated Hammer"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["name"], "Updated Hammer")

    def test_delete_product(self):
        product_id = self.create_product()
        response = self.client.delete(f"/products/{product_id}")
        self.assertEqual(response.status_code, 204)

    def test_list_all_products(self):
        self.create_product()
        response = self.client.get("/products")
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.get_json()), 1)

    def test_list_by_name(self):
        self.create_product(name="Hammer")
        response = self.client.get("/products?name=Hammer")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            all(p["name"] == "Hammer" for p in response.get_json())
        )

    def test_list_by_category(self):
        self.create_product(category=Category.TOOLS)
        response = self.client.get("/products?category=TOOLS")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            all(p["category"] == "TOOLS" for p in response.get_json())
        )

    def test_list_by_availability(self):
        self.create_product(available=True)
        response = self.client.get("/products?available=true")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            all(p["available"] is True for p in response.get_json())
        )


if __name__ == "__main__":
    unittest.main()
