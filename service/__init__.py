
"""Product Catalogue service package."""

from flask import Flask
from service.models import db


def create_app(test_config=None):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI="sqlite:///products.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config:
        app.config.update(test_config)

    db.init_app(app)

    from service.routes import register_routes
    register_routes(app)

    with app.app_context():
        db.create_all()

    return app
