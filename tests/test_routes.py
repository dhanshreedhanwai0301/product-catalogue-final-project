
"""Tests for the Product REST API routes."""

import unittest
from flask import Flask

from service.models import db, Product, Category
from service.routes import app


class TestProductRoutes(unittest.TestCase):
    """Test product API endpoints."""

    def setUp(self):
        self.app = app
        self.app.config["TESTING"] = True
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        self.client = self.app.test_client()

        with self.app.app_context():
            db.drop_all()
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def create_product(self, name="Hammer", category=Category.TOOLS,
                       available=True):
        product = Product(
            name=name,
            description="Test product",
            price=10.00,
            category=category,
            available=available,
        )
        db.session.add(product)
        db.session.commit()
        return product

    def test_read_product(self):
        product = self.create_product()
        response = self.client.get(f"/products/{product.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["name"], "Hammer")

    def test_update_product(self):
        product = self.create_product()
        response = self.client.put(
            f"/products/{product.id}",
            json={"name": "Updated Hammer"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["name"], "Updated Hammer")

    def test_delete_product(self):
        product = self.create_product()
        response = self.client.delete(f"/products/{product.id}")
        self.assertIn(response.status_code, (200, 204))

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
            all(item["name"] == "Hammer" for item in response.get_json())
        )

    def test_list_by_category(self):
        self.create_product(category=Category.TOOLS)
        response = self.client.get("/products?category=TOOLS")
        self.assertEqual(response.status_code, 200)

    def test_list_by_availability(self):
        self.create_product(available=True)
        response = self.client.get("/products?available=true")
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
