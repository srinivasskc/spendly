# Step 1: Database Setup

## Overview
Set up SQLite database with users and expenses tables, and implement the database helper functions in `database/db.py`.

## Requirements

### 1. Database File Location
- Database file: `spendly.db` in project root
- SQLite database

### 2. Tables

#### users
| Column | Type | Constraints |
|--------|------|-------------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT |
| name | TEXT | NOT NULL |
| email | TEXT | NOT NULL UNIQUE |
| password | TEXT | NOT NULL (hashed) |
| created_at | TEXT | NOT NULL (ISO 8601 timestamp) |

#### expenses
| Column | Type | Constraints |
|--------|------|-------------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT |
| user_id | INTEGER | NOT NULL, FOREIGN KEY → users(id) ON DELETE CASCADE |
| amount | REAL | NOT NULL |
| description | TEXT | NOT NULL |
| category | TEXT | NOT NULL |
| date | TEXT | NOT NULL (ISO 8601 date) |
| created_at | TEXT | NOT NULL (ISO 8601 timestamp) |

### 3. Helper Functions (database/db.py)

#### `get_db()`
- Opens connection to `spendly.db`
- Sets `row_factory = sqlite3.Row` for dict-like row access
- Enables foreign keys: `PRAGMA foreign_keys = ON`
- Returns the connection

#### `init_db()`
- Creates all tables using `CREATE TABLE IF NOT EXISTS`
- Runs `PRAGMA foreign_keys = ON` after table creation
- Called once during app initialization

#### `seed_db()`
- Inserts sample data for development:
  - 1 sample user (pre-hashed password)
  - 5 sample expenses linked to that user
- Should be safe to run multiple times (or check before inserting)

## Acceptance Criteria
- [ ] `get_db()` returns a connection with row_factory and foreign keys enabled
- [ ] `init_db()` creates both tables with correct schemas
- [ ] `seed_db()` inserts sample user and expenses
- [ ] Foreign key cascade delete works on expenses when user is deleted
- [ ] All queries use parameterized placeholders (`?`), never f-strings

## Notes
- Passwords should be hashed (use Python's `hashlib` or `werkzeug.security`)
- Use ISO 8601 format for all timestamps and dates
- Currency is INR (Indian Rupees)