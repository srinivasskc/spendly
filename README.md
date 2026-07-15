# Spendly - Personal Expense Tracker

Spendly is a lightweight personal expense tracker built with Flask and SQLite. Track your daily expenses, view summaries, and manage your finances with a simple, clean interface.

---

## Features

- **User Authentication** - Register and login with secure password hashing
- **Track Expenses** - Add, edit, and delete expense entries
- **Categories** - Organize expenses by category (Food, Transport, Shopping, Bills, Entertainment, etc.)
- **Dashboard** - View expense summary and recent transactions on your profile
- **INR Currency** - All amounts in Indian Rupees (₹)

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| Backend | Flask (Python) |
| Database | SQLite |
| Frontend | HTML, CSS, Vanilla JavaScript |
| Testing | pytest |

---

## Project Structure

```
spendly/
├── app.py              # All Flask routes (no blueprints)
├── database/
│   ├── __init__.py
│   └── db.py           # SQLite helpers and queries
├── templates/
│   ├── base.html       # Shared layout
│   ├── landing.html    # Landing page
│   ├── register.html   # Registration form
│   ├── login.html      # Login form
│   ├── profile.html    # User dashboard
│   ├── expense_add.html
│   ├── expense_edit.html
│   ├── terms.html
│   └── privacy.html
├── static/
│   ├── css/
│   │   ├── style.css
│   │   ├── landing.css
│   │   ├── profile.css
│   │   └── expense.css
│   └── js/
│       └── main.js
├── tests/              # Pytest test files
├── requirements.txt
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.10 or higher

### Installation

1. **Clone the repository**
   ```bash
   cd expense-tracker
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**

   Windows:
   ```bash
   venv\Scripts\activate
   ```

   macOS/Linux:
   ```bash
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Initialize the database**
   
   The database is automatically created when you run the app. To manually initialize:
   ```python
   from database.db import init_db, seed_db
   init_db()      # Creates tables
   seed_db()      # Adds sample data (optional)
   ```

### Running the App

```bash
python app.py
```

The app will start on **http://localhost:5001**

---

## Usage Guide

### 1. Register an Account
- Visit `/register` to create a new account
- Password must be at least 8 characters

### 2. Login
- Visit `/login` with your credentials
- Session-based authentication

### 3. Add Expenses
- Navigate to **Add Expense** from your profile
- Enter amount (in INR), description, category, and date
- Categories: Food, Transport, Shopping, Bills, Entertainment, Health, Other

### 4. Manage Expenses
- Edit existing expenses via the edit button
- Delete expenses via the delete button (requires confirmation)

### 5. View Dashboard
- Your profile shows total expenses and recent transactions

### 6. Logout
- Click logout to end your session

---

## Available Routes

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Landing page |
| `/register` | GET, POST | User registration |
| `/login` | GET, POST | User login |
| `/logout` | GET | User logout |
| `/profile` | GET | User dashboard |
| `/expenses/add` | GET, POST | Add new expense |
| `/expenses/<id>/edit` | GET, POST | Edit expense |
| `/expenses/<id>/delete` | POST | Delete expense |
| `/terms` | GET | Terms of service |
| `/privacy` | GET | Privacy policy |

---

## Testing

The project uses pytest for testing. Tests are located in the `tests/` directory.

### Running Tests

```bash
# Run all tests
pytest

# Run a specific test file
pytest tests/test_filename.py

# Run with output visible
pytest -s
```

### Test Subagents

The project includes Claude subagents for testing:

- **spendly-test-writer**: Generates pytest tests based on feature specifications
- **spendly-test-runner**: Executes and analyzes test results

Invoke these subagents after implementing features to generate and run tests.

---

## Development Notes

- **Database**: SQLite (`spendly.db` in the project root)
- **Secret Key**: Change `app.secret_key` in `app.py` before production
- **No ORM**: Direct SQLite queries using parameterized statements
- **Foreign Keys**: Enabled via `PRAGMA foreign_keys = ON`
- **Passwords**: Hashed using Werkzeug's `generate_password_hash`

---

## License

MIT License