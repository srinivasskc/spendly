import sqlite3
import os
from datetime import datetime
from werkzeug.security import generate_password_hash

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
DB_PATH = os.path.join(BASE_DIR, "spendly.db")


def get_db():
    """Return a SQLite connection with row_factory and foreign keys enabled."""
    # Try to get database path from Flask app config, fallback to default
    try:
        from flask import current_app
        db_path = current_app.config.get('DATABASE', DB_PATH)
    except RuntimeError:
        db_path = DB_PATH

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Create all tables if they don't exist."""
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            description TEXT NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
    """)
    conn.commit()
    conn.close()


def get_user_by_email(email):
    """Retrieve a user by email address."""
    conn = get_db()
    user = conn.execute(
        "SELECT id, name, email, password, created_at FROM users WHERE email = ?",
        (email,)
    ).fetchone()
    conn.close()
    return user


def get_user_by_id(user_id):
    """Retrieve a user by ID."""
    conn = get_db()
    user = conn.execute(
        "SELECT id, name, email, created_at FROM users WHERE id = ?",
        (user_id,)
    ).fetchone()
    conn.close()
    return user


def get_expense_summary(user_id):
    """Get expense summary: total count and total amount."""
    conn = get_db()
    result = conn.execute(
        "SELECT COUNT(*) as count, COALESCE(SUM(amount), 0) as total FROM expenses WHERE user_id = ?",
        (user_id,)
    ).fetchone()
    conn.close()
    return {"count": result["count"], "total": result["total"]}


def get_recent_expenses(user_id, limit=5):
    """Get recent expenses for a user, ordered by date descending."""
    conn = get_db()
    results = conn.execute(
        "SELECT id, amount, description, category, date FROM expenses WHERE user_id = ? ORDER BY date DESC, id DESC LIMIT ?",
        (user_id, limit)
    ).fetchall()
    conn.close()
    return [dict(row) for row in results]


def add_expense(user_id, amount, description, category, date):
    """Insert a new expense into the database."""
    conn = get_db()
    created_at = datetime.now().isoformat()
    conn.execute(
        "INSERT INTO expenses (user_id, amount, description, category, date, created_at) VALUES (?, ?, ?, ?, ?, ?)",
        (user_id, amount, description, category, date, created_at)
    )
    conn.commit()
    conn.close()


def get_expense_by_id(expense_id):
    """Get a single expense by ID."""
    conn = get_db()
    expense = conn.execute(
        "SELECT id, user_id, amount, description, category, date FROM expenses WHERE id = ?",
        (expense_id,)
    ).fetchone()
    conn.close()
    return dict(expense) if expense else None


def update_expense(expense_id, amount, description, category, date):
    """Update an existing expense."""
    conn = get_db()
    conn.execute(
        "UPDATE expenses SET amount = ?, description = ?, category = ?, date = ? WHERE id = ?",
        (amount, description, category, date, expense_id)
    )
    conn.commit()
    conn.close()


def delete_expense(expense_id):
    """Delete an expense from the database."""
    conn = get_db()
    conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()


def get_filtered_expenses(user_id, start_date=None, end_date=None, limit=None):
    """Get expenses for a user filtered by date range."""
    conn = get_db()
    query = "SELECT id, amount, description, category, date FROM expenses WHERE user_id = ?"
    params = [user_id]

    if start_date:
        query += " AND date >= ?"
        params.append(start_date)
    if end_date:
        query += " AND date <= ?"
        params.append(end_date)

    query += " ORDER BY date DESC, id DESC"

    if limit:
        query += " LIMIT ?"
        params.append(limit)

    results = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(row) for row in results]


def get_expense_summary_filtered(user_id, start_date=None, end_date=None):
    """Get expense summary filtered by date range."""
    conn = get_db()
    query = "SELECT COUNT(*) as count, COALESCE(SUM(amount), 0) as total FROM expenses WHERE user_id = ?"
    params = [user_id]

    if start_date:
        query += " AND date >= ?"
        params.append(start_date)
    if end_date:
        query += " AND date <= ?"
        params.append(end_date)

    result = conn.execute(query, params).fetchone()
    conn.close()
    return {"count": result["count"], "total": result["total"]}


def get_all_categories_for_user(user_id):
    """Get all unique categories used by a user."""
    conn = get_db()
    results = conn.execute(
        "SELECT DISTINCT category FROM expenses WHERE user_id = ? ORDER BY category",
        (user_id,)
    ).fetchall()
    conn.close()
    return [row["category"] for row in results]


def seed_db():
    """Insert sample data for development if no users exist."""
    conn = get_db()

    # Check if sample data already exists
    existing = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    if existing > 0:
        conn.close()
        return

    # Insert sample user (password: "testpass123" - hashed)
    hashed_password = generate_password_hash("testpass123")
    now = datetime.now().isoformat()

    conn.execute(
        "INSERT INTO users (name, email, password, created_at) VALUES (?, ?, ?, ?)",
        ("Test User", "test@example.com", hashed_password, now)
    )

    # Get the user's id
    user_id = conn.execute("SELECT id FROM users WHERE email = ?", ("test@example.com",)).fetchone()[0]

    # Insert sample expenses
    expenses = [
        (user_id, 250.00, "Lunch at restaurant", "Food", "2026-06-01", now),
        (user_id, 50.00, "Auto rickshaw", "Transport", "2026-06-02", now),
        (user_id, 1500.00, "New headphones", "Shopping", "2026-06-03", now),
        (user_id, 1200.00, "Electricity bill", "Bills", "2026-06-01", now),
        (user_id, 400.00, "Movie tickets", "Entertainment", "2026-06-04", now),
    ]

    conn.executemany(
        "INSERT INTO expenses (user_id, amount, description, category, date, created_at) VALUES (?, ?, ?, ?, ?, ?)",
        expenses
    )

    conn.commit()
    conn.close()