
"""REST API routes for the Product Catalogue."""

from flask import jsonify, request
from service.models import db, Product, Category


def register_routes(app):
    """Register product endpoints on the Flask application."""

    @app.route("/products/<int:product_id>", methods=["GET"])
    def read_product(product_id):
        """Read a product by ID."""
        product = db.session.get(Product, product_id)
        if product is None:
            return jsonify(error="Product not found"), 404
        return jsonify(product.serialize()), 200

    @app.route("/products/<int:product_id>", methods=["PUT"])
    def update_product(product_id):
        """Update a product."""
        product = db.session.get(Product, product_id)
        if product is None:
            return jsonify(error="Product not found"), 404

        data = request.get_json(silent=True) or {}

        if "name" in data:
            product.name = data["name"]
        if "description" in data:
            product.description = data["description"]
        if "price" in data:
            product.price = data["price"]
        if "available" in data:
            product.available = data["available"]
        if "category" in data:
            try:
                product.category = Category[data["category"].upper()]
            except (KeyError, AttributeError):
                return jsonify(error="Invalid category"), 400

        db.session.commit()
        return jsonify(product.serialize()), 200

    @app.route("/products/<int:product_id>", methods=["DELETE"])
    def delete_product(product_id):
        """Delete a product."""
        product = db.session.get(Product, product_id)
        if product is None:
            return jsonify(error="Product not found"), 404

        db.session.delete(product)
        db.session.commit()
        return "", 204

    @app.route("/products", methods=["GET"])
    def list_products():
        """List products with optional filters."""
        query = Product.query

        name = request.args.get("name")
        category = request.args.get("category")
        available = request.args.get("available")

        if name:
            query = query.filter(Product.name.ilike(f"%{name}%"))

        if category:
            try:
                category_value = Category[category.upper()]
            except KeyError:
                return jsonify(error="Invalid category"), 400
            query = query.filter_by(category=category_value)

        if available is not None:
            if available.lower() not in ("true", "false"):
                return jsonify(error="Invalid availability"), 400
            query = query.filter_by(
                available=available.lower() == "true"
            )

        return jsonify([p.serialize() for p in query.all()]), 200
