
"""Behave environment setup for the Product Catalogue."""

import threading
import time

from werkzeug.serving import make_server
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from service import create_app
from service.models import db


def before_all(context):
    """Start the Flask server and Selenium browser."""
    context.app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:////tmp/product_bdd.db",
    })

    context.server = make_server("127.0.0.1", 5000, context.app)
    context.server_thread = threading.Thread(
        target=context.server.serve_forever,
        daemon=True,
    )
    context.server_thread.start()
    time.sleep(1)

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    context.browser = webdriver.Chrome(options=options)
    context.base_url = "http://127.0.0.1:5000"


def before_scenario(context, scenario):
    """Reset the product database before each scenario."""
    with context.app.app_context():
        db.session.remove()
        db.drop_all()
        db.create_all()

    context.browser.get(context.base_url)


def after_all(context):
    """Close Selenium and stop the Flask server."""
    if getattr(context, "browser", None):
        context.browser.quit()

    if getattr(context, "server", None):
        context.server.shutdown()
        context.server_thread.join(timeout=5)

    with context.app.app_context():
        db.session.remove()
        db.drop_all()
