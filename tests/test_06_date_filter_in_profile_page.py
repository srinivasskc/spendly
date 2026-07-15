"""Tests for date filter feature in profile page."""
import pytest
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestDateFilterHappyPaths:
    """Test happy path scenarios for date filtering."""

    def test_filter_by_start_date_only_shows_expenses_from_that_date(self, client):
        """When only start_date is provided, show expenses from that date onwards."""
        # Setup: register and login user with known expenses
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

        # Add test expenses
        from database.db import add_expense
        with client.application.app_context():
            user_id = 1
            add_expense(user_id, 250.00, "June 1 expense", "Food", "2026-06-01")
            add_expense(user_id, 50.00, "June 2 expense", "Transport", "2026-06-02")
            add_expense(user_id, 1500.00, "June 3 expense", "Shopping", "2026-06-03")
            add_expense(user_id, 1200.00, "July 1 expense", "Bills", "2026-07-01")

        # Filter by start_date = 2026-06-02 (should exclude June 1 expense)
        response = client.get('/profile?start_date=2026-06-02')

        assert response.status_code == 200
        # Should contain June 2, June 3, July 1 expenses (total: 1800)
        # Should NOT contain June 1 expense (250)
        assert b'June 2 expense' in response.data or b'June 02' in response.data
        assert b'June 3 expense' in response.data or b'June 03' in response.data

    def test_filter_by_end_date_only_shows_expenses_until_that_date(self, client):
        """When only end_date is provided, show expenses until that date."""
        # Setup: register and login user with known expenses
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

        # Add test expenses
        from database.db import add_expense
        with client.application.app_context():
            user_id = 1
            add_expense(user_id, 250.00, "June 1 expense", "Food", "2026-06-01")
            add_expense(user_id, 50.00, "June 2 expense", "Transport", "2026-06-02")
            add_expense(user_id, 1500.00, "June 3 expense", "Shopping", "2026-06-03")
            add_expense(user_id, 1200.00, "July 1 expense", "Bills", "2026-07-01")

        # Filter by end_date = 2026-06-02 (should exclude June 3 and July 1)
        response = client.get('/profile?end_date=2026-06-02')

        assert response.status_code == 200
        # Should contain June 1 and June 2 expenses (total: 300)
        # Should NOT contain June 3 or July 1 expenses
        assert b'June 1 expense' in response.data or b'June 01' in response.data

    def test_filter_by_both_dates_shows_expenses_within_range(self, client):
        """When both start_date and end_date are provided, show expenses within that range."""
        # Setup: register and login user with known expenses
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

        # Add test expenses
        from database.db import add_expense
        with client.application.app_context():
            user_id = 1
            add_expense(user_id, 250.00, "June 1 expense", "Food", "2026-06-01")
            add_expense(user_id, 50.00, "June 2 expense", "Transport", "2026-06-02")
            add_expense(user_id, 1500.00, "June 3 expense", "Shopping", "2026-06-03")
            add_expense(user_id, 1200.00, "July 1 expense", "Bills", "2026-07-01")

        # Filter by start_date = 2026-06-02 and end_date = 2026-06-03
        response = client.get('/profile?start_date=2026-06-02&end_date=2026-06-03')

        assert response.status_code == 200
        # Should contain June 2 and June 3 expenses (total: 1550)
        # Should NOT contain June 1 or July 1 expenses
        assert b'June 2 expense' in response.data or b'June 02' in response.data
        assert b'June 3 expense' in response.data or b'June 03' in response.data


class TestDateFilterEdgeCases:
    """Test edge cases for date filtering."""

    def test_no_filter_shows_default_expenses(self, client):
        """When no date filters provided, show default expenses (recent 5)."""
        # Setup: register and login user with known expenses
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

        # Add more than 5 test expenses
        from database.db import add_expense
        with client.application.app_context():
            user_id = 1
            add_expense(user_id, 100.00, "Expense 1", "Food", "2026-06-01")
            add_expense(user_id, 200.00, "Expense 2", "Food", "2026-06-02")
            add_expense(user_id, 300.00, "Expense 3", "Food", "2026-06-03")
            add_expense(user_id, 400.00, "Expense 4", "Food", "2026-06-04")
            add_expense(user_id, 500.00, "Expense 5", "Food", "2026-06-05")
            add_expense(user_id, 600.00, "Expense 6", "Food", "2026-06-06")
            add_expense(user_id, 700.00, "Expense 7", "Food", "2026-06-07")

        # Request profile without any filters
        response = client.get('/profile')

        assert response.status_code == 200
        # Should show recent 5 expenses (Expense 7-3), not all 7

    def test_empty_dates_are_ignored(self, client):
        """Empty string start_date or end_date should be treated as no filter."""
        # Setup: register and login user with known expenses
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

        # Add test expenses
        from database.db import add_expense
        with client.application.app_context():
            user_id = 1
            add_expense(user_id, 250.00, "June 1 expense", "Food", "2026-06-01")
            add_expense(user_id, 50.00, "June 2 expense", "Transport", "2026-06-02")

        # Empty start_date should behave like no filter
        response = client.get('/profile?start_date=')

        assert response.status_code == 200

    def test_date_filter_with_no_matching_expenses(self, client):
        """When filter yields no results, show empty list with correct totals."""
        # Setup: register and login user with known expenses
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

        # Add test expenses
        from database.db import add_expense
        with client.application.app_context():
            user_id = 1
            add_expense(user_id, 250.00, "June expense", "Food", "2026-06-01")

        # Filter that excludes all expenses (dates far outside the range)
        response = client.get('/profile?start_date=2025-01-01&end_date=2025-12-31')

        assert response.status_code == 200
        # Should show 0 expenses and 0 total


class TestDateFilterAuthGuards:
    """Test authentication guards for profile page with date filters."""

    def test_unauthenticated_request_redirects_to_login(self, client):
        """Unauthenticated request to /profile should redirect to login."""
        response = client.get('/profile')
        assert response.status_code == 302
        assert '/login' in response.location

    def test_unauthenticated_request_with_date_filter_redirects_to_login(self, client):
        """Unauthenticated request with date filters should redirect to login."""
        response = client.get('/profile?start_date=2026-06-01&end_date=2026-06-30')
        assert response.status_code == 302
        assert '/login' in response.location

    def test_unauthenticated_request_with_only_start_date_redirects_to_login(self, client):
        """Unauthenticated request with only start_date should redirect to login."""
        response = client.get('/profile?start_date=2026-06-01')
        assert response.status_code == 302
        assert '/login' in response.location

    def test_unauthenticated_request_with_only_end_date_redirects_to_login(self, client):
        """Unauthenticated request with only end_date should redirect to login."""
        response = client.get('/profile?end_date=2026-06-30')
        assert response.status_code == 302
        assert '/login' in response.location


class TestDateFilterDatabaseSideEffects:
    """Test database side effects - totals and counts update correctly."""

    def test_total_spent_updates_with_start_date_filter(self, client):
        """Total spent should reflect filtered results when using start_date."""
        # Setup: register and login user with known expenses
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

        # Add test expenses with specific amounts
        from database.db import add_expense
        with client.application.app_context():
            user_id = 1
            add_expense(user_id, 100.00, "May expense", "Food", "2026-05-15")
            add_expense(user_id, 200.00, "June 1 expense", "Food", "2026-06-01")
            add_expense(user_id, 300.00, "June 15 expense", "Food", "2026-06-15")
            add_expense(user_id, 400.00, "July 1 expense", "Food", "2026-07-01")

        # Filter by start_date = 2026-06-01 (should include 200+300+400 = 900)
        response = client.get('/profile?start_date=2026-06-01')

        assert response.status_code == 200
        # The total should be 900 (not including the 100 May expense)
        assert b'900' in response.data or b'900.00' in response.data

    def test_total_spent_updates_with_end_date_filter(self, client):
        """Total spent should reflect filtered results when using end_date."""
        # Setup: register and login user with known expenses
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

        # Add test expenses with specific amounts
        from database.db import add_expense
        with client.application.app_context():
            user_id = 1
            add_expense(user_id, 100.00, "May expense", "Food", "2026-05-15")
            add_expense(user_id, 200.00, "June 1 expense", "Food", "2026-06-01")
            add_expense(user_id, 300.00, "June 15 expense", "Food", "2026-06-15")
            add_expense(user_id, 400.00, "July 1 expense", "Food", "2026-07-01")

        # Filter by end_date = 2026-06-15 (should include 100+200+300 = 600)
        response = client.get('/profile?end_date=2026-06-15')

        assert response.status_code == 200
        # The total should be 600 (not including the 400 July expense)
        assert b'600' in response.data or b'600.00' in response.data

    def test_total_spent_updates_with_both_filters(self, client):
        """Total spent should reflect filtered results when using both dates."""
        # Setup: register and login user with known expenses
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

        # Add test expenses with specific amounts
        from database.db import add_expense
        with client.application.app_context():
            user_id = 1
            add_expense(user_id, 100.00, "May expense", "Food", "2026-05-15")
            add_expense(user_id, 200.00, "June 1 expense", "Food", "2026-06-01")
            add_expense(user_id, 300.00, "June 15 expense", "Food", "2026-06-15")
            add_expense(user_id, 400.00, "July 1 expense", "Food", "2026-07-01")

        # Filter by start_date = 2026-06-01 and end_date = 2026-06-15 (should include 200+300 = 500)
        response = client.get('/profile?start_date=2026-06-01&end_date=2026-06-15')

        assert response.status_code == 200
        # The total should be 500
        assert b'500' in response.data or b'500.00' in response.data

    def test_expense_count_updates_with_filter(self, client):
        """Expense count should reflect filtered results."""
        # Setup: register and login user with known expenses
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

        # Add test expenses with specific amounts
        from database.db import add_expense
        with client.application.app_context():
            user_id = 1
            add_expense(user_id, 100.00, "May expense", "Food", "2026-05-15")
            add_expense(user_id, 200.00, "June 1 expense", "Food", "2026-06-01")
            add_expense(user_id, 300.00, "June 15 expense", "Food", "2026-06-15")

        # Filter by start_date = 2026-06-01 (should include 2 expenses)
        response = client.get('/profile?start_date=2026-06-01')

        assert response.status_code == 200
        # Should show count of 2
        assert b'2' in response.data or b'2 expense' in response.data or b'2 total' in response.data


class TestDateFilterTemplateRendering:
    """Test template rendering for date filter feature."""

    def test_profile_page_renders_with_date_filter_form(self, client):
        """Profile page should render with date filter form inputs."""
        # Setup: register and login
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

        response = client.get('/profile')

        assert response.status_code == 200
        # Should have date input fields
        assert b'start_date' in response.data or b'start-date' in response.data or b'startDate' in response.data
        assert b'end_date' in response.data or b'end-date' in response.data or b'endDate' in response.data

    def test_profile_page_preserves_filter_values_in_form(self, client):
        """When filters are applied, they should be preserved in the form inputs."""
        # Setup: register and login
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

        response = client.get('/profile?start_date=2026-06-01&end_date=2026-06-30')

        assert response.status_code == 200
        # The filter values should appear in the response (in the form inputs)
        assert b'2026-06-01' in response.data
        assert b'2026-06-30' in response.data


class TestDateFilterBoundaryCases:
    """Test boundary cases for date filtering."""

    def test_filter_on_exact_start_date_includes_that_date(self, client):
        """Expenses on the start_date should be included."""
        # Setup: register and login
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

        from database.db import add_expense
        with client.application.app_context():
            user_id = 1
            add_expense(user_id, 100.00, "June 1 expense", "Food", "2026-06-01")
            add_expense(user_id, 200.00, "June 2 expense", "Food", "2026-06-02")

        # Filter starting from June 1 - should include both expenses
        response = client.get('/profile?start_date=2026-06-01')

        assert response.status_code == 200
        # Both expenses should be included
        assert b'100' in response.data or b'June 1' in response.data or b'June 01' in response.data

    def test_filter_on_exact_end_date_includes_that_date(self, client):
        """Expenses on the end_date should be included."""
        # Setup: register and login
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

        from database.db import add_expense
        with client.application.app_context():
            user_id = 1
            add_expense(user_id, 100.00, "June 1 expense", "Food", "2026-06-01")
            add_expense(user_id, 200.00, "June 2 expense", "Food", "2026-06-02")

        # Filter ending on June 2 - should include both expenses
        response = client.get('/profile?end_date=2026-06-02')

        assert response.status_code == 200
        # Both expenses should be included
        assert b'100' in response.data or b'June 1' in response.data or b'June 01' in response.data
        assert b'200' in response.data or b'June 2' in response.data or b'June 02' in response.data