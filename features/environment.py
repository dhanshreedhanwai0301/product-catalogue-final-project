
"""Behave environment setup for Product Catalogue tests."""

from service import create_app
from service.models import db


def before_all(context):
    """Initialize the Flask application and browser."""
    context.app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })
    context.browser = None


def before_scenario(context, scenario):
    """Prepare a clean database for each scenario."""
    with context.app.app_context():
        db.drop_all()
        db.create_all()


def after_all(context):
    """Clean up the browser and database."""
    if context.browser is not None:
        context.browser.quit()

    with context.app.app_context():
        db.session.remove()
        db.drop_all()
