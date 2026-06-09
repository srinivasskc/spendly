import sqlite3
import os
from datetime import datetime
from werkzeug.security import generate_password_hash

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
DB_PATH = os.path.join(BASE_DIR, "spendly.db")


def get_db():
    """Return a SQLite connection with row_factory and foreign keys enabled."""
    conn = sqlite3.connect(DB_PATH)
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