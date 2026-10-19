
"""Product model for the catalogue service."""

from enum import Enum

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Category(Enum):
    """Product categories."""

    UNKNOWN = 0
    CLOTHS = 1
    FOOD = 2
    HOUSEWARES = 3
    AUTOMOTIVE = 4
    TOOLS = 5


class Product(db.Model):
    """Represents a product in the catalogue."""

    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(256))
    price = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    available = db.Column(db.Boolean, nullable=False, default=True)
    category = db.Column(
        db.Enum(Category),
        nullable=False,
        default=Category.UNKNOWN,
    )

    def serialize(self):
        """Convert a product to a dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": float(self.price),
            "available": self.available,
            "category": self.category.name,
        }
