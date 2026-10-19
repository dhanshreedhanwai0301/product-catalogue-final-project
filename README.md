
# Product Catalogue Final Project

A Python product catalogue API using Flask and Flask-SQLAlchemy, with
model tests, REST API tests, and Behave/Selenium BDD scenarios.

## Features

- Read, update, and delete products
- List all products
- Search products by name, category, and availability
- Automated model and API tests
- BDD feature scenarios and Selenium step definitions

## Main files

- `service/models.py` — Product model and categories
- `service/routes.py` — REST API routes
- `tests/factories.py` — Fake product factory
- `tests/test_models.py` — Model tests
- `tests/test_routes.py` — API route tests
- `features/steps/load_steps.py` — BDD background data
- `features/products.feature` — BDD scenarios
- `features/steps/web_steps.py` — Selenium step definitions
