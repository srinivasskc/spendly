"""Pytest fixtures for Spendly expense tracker tests."""
import pytest
import sys
import os
import tempfile

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app as flask_app
from database.db import init_db, get_db, add_expense


@pytest.fixture
def app(tmp_path):
    """Create test app with temporary database."""
    test_db = tmp_path / "test_spendly.db"
    flask_app.config.update({
        'TESTING': True,
        'DATABASE': str(test_db),
        'SECRET_KEY': 'test-secret-key',
        'WTF_CSRF_ENABLED': False,
    })
    with flask_app.app_context():
        init_db()
        yield flask_app


@pytest.fixture
def client(app):
    """Flask test client."""
    return app.test_client()


@pytest.fixture
def auth_client(client):
    """A test client that is already logged in with test data."""
    # Register and login a test user
    client.post('/register', data={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'testpass123',
        'confirm_password': 'testpass123'
    })
    client.post('/login', data={
        'email': 'test@example.com',
        'password': 'testpass123'
    })

    # Add test expenses with known dates
    with flask_app.app_context():
        user_id = 1  # First user
        add_expense(user_id, 250.00, "Lunch at restaurant", "Food", "2026-06-01")
        add_expense(user_id, 50.00, "Auto rickshaw", "Transport", "2026-06-02")
        add_expense(user_id, 1500.00, "New headphones", "Shopping", "2026-06-03")
        add_expense(user_id, 1200.00, "Electricity bill", "Bills", "2026-06-01")
        add_expense(user_id, 400.00, "Movie tickets", "Entertainment", "2026-06-04")
        add_expense(user_id, 300.00, "Groceries", "Food", "2026-07-01")
        add_expense(user_id, 750.00, "Gas cylinder", "Bills", "2026-07-10")

    return client


@pytest.fixture
def app_with_expenses(app):
    """App with sample expenses for testing."""
    with app.app_context():
        user_id = 1
        add_expense(user_id, 250.00, "Lunch at restaurant", "Food", "2026-06-01")
        add_expense(user_id, 50.00, "Auto rickshaw", "Transport", "2026-06-02")
        add_expense(user_id, 1500.00, "New headphones", "Shopping", "2026-06-03")
        add_expense(user_id, 1200.00, "Electricity bill", "Bills", "2026-06-01")
        add_expense(user_id, 400.00, "Movie tickets", "Entertainment", "2026-06-04")
        add_expense(user_id, 300.00, "Groceries", "Food", "2026-07-01")
        add_expense(user_id, 750.00, "Gas cylinder", "Bills", "2026-07-10")
    return app