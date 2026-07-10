from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
import re

from database.db import get_db, get_user_by_email, get_user_by_id, get_expense_summary, get_recent_expenses
from database.db import add_expense as db_add_expense, get_expense_by_id as db_get_expense_by_id, update_expense as db_update_expense, delete_expense as db_delete_expense

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__,
            template_folder=os.path.join(BASE_DIR, "templates"),
            static_folder=os.path.join(BASE_DIR, "static"),
            instance_path=os.path.join(BASE_DIR, "instance"))
app.secret_key = "dev-secret-key-change-in-production"

# Ensure instance folder exists
os.makedirs(app.instance_path, exist_ok=True)

# DON'T initialize database yet - test if templates work first


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    # POST request - process registration
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")
    confirm_password = request.form.get("confirm_password", "")

    # Server-side validation
    if not name or not email or not password or not confirm_password:
        return render_template("register.html", error="All fields are required.")

    if len(password) < 8:
        return render_template("register.html", error="Password must be at least 8 characters.")

    if password != confirm_password:
        return render_template("register.html", error="Passwords do not match.")

    # Basic email format validation
    email_pattern = r'^[^@\s]+@[^@\s]+\.[^@\s]+$'
    if not re.match(email_pattern, email):
        return render_template("register.html", error="Please enter a valid email address.")

    # Check if email already exists
    conn = get_db()
    existing_user = conn.execute(
        "SELECT id FROM users WHERE email = ?",
        (email,)
    ).fetchone()
    conn.close()

    if existing_user:
        return render_template("register.html", error="An account with this email already exists.")

    # Hash password and create user
    hashed_password = generate_password_hash(password)
    created_at = datetime.now().isoformat()

    conn = get_db()
    conn.execute(
        "INSERT INTO users (name, email, password, created_at) VALUES (?, ?, ?, ?)",
        (name, email, hashed_password, created_at)
    )
    conn.commit()
    conn.close()

    flash("Registration successful! Please sign in.")
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    # POST request - process login
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")

    # Validate fields
    if not email or not password:
        return render_template("login.html", error="Email and password are required.")

    # Get user by email
    user = get_user_by_email(email)

    if not user:
        return render_template("login.html", error="Invalid email or password.")

    # Verify password
    if not check_password_hash(user["password"], password):
        return render_template("login.html", error="Invalid email or password.")

    # Create session
    session["user_id"] = user["id"]
    session["user_name"] = user["name"]
    session["user_email"] = user["email"]

    flash("Welcome back! You have signed in successfully.")
    return redirect(url_for("profile"))


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been signed out.")
    return redirect(url_for("landing"))


@app.route("/profile")
def profile():
    # Check authentication
    user_id = session.get("user_id")
    if not user_id:
        flash("Please sign in to view your profile.")
        return redirect(url_for("login"))

    # Fetch user data
    user = get_user_by_id(user_id)
    if not user:
        session.clear()
        return redirect(url_for("login"))

    # Fetch expense summary
    summary = get_expense_summary(user_id)
    recent_expenses = get_recent_expenses(user_id, limit=5)

    # Format member since date
    try:
        created = datetime.fromisoformat(user["created_at"])
        member_since = created.strftime("%B %Y")  # e.g., "June 2026"
    except:
        member_since = "Unknown"

    return render_template(
        "profile.html",
        user=user,
        expense_count=summary["count"],
        total_spent=summary["total"],
        member_since=member_since,
        recent_expenses=recent_expenses
    )


@app.route("/expenses/add", methods=["GET", "POST"])
def add_expense():
    # Check authentication
    user_id = session.get("user_id")
    if not user_id:
        flash("Please sign in to add an expense.")
        return redirect(url_for("login"))

    if request.method == "GET":
        return render_template("expense_add.html")

    # POST request - process form data
    amount = request.form.get("amount", "").strip()
    description = request.form.get("description", "").strip()
    category = request.form.get("category", "").strip()
    date = request.form.get("date", "").strip()

    # Server-side validation
    if not amount or not description or not category or not date:
        return render_template("expense_add.html", error="All fields are required.")

    try:
        amount = float(amount)
        if amount <= 0:
            return render_template("expense_add.html", error="Amount must be greater than 0.")
    except ValueError:
        return render_template("expense_add.html", error="Please enter a valid amount.")

    # Insert expense into database
    db_add_expense(user_id, amount, description, category, date)

    flash("Expense added successfully!")
    return redirect(url_for("profile"))


@app.route("/expenses/<int:id>/edit", methods=["GET", "POST"])
def edit_expense(id):
    # Check authentication
    user_id = session.get("user_id")
    if not user_id:
        flash("Please sign in to edit an expense.")
        return redirect(url_for("login"))

    # Get expense and verify ownership
    expense = db_get_expense_by_id(id)
    if not expense:
        flash("Expense not found.")
        return redirect(url_for("profile"))

    if expense["user_id"] != user_id:
        flash("You don't have permission to edit this expense.")
        return redirect(url_for("profile"))

    if request.method == "GET":
        return render_template("expense_edit.html", expense=expense)

    # POST request - process form data
    amount = request.form.get("amount", "").strip()
    description = request.form.get("description", "").strip()
    category = request.form.get("category", "").strip()
    date = request.form.get("date", "").strip()

    # Server-side validation
    if not amount or not description or not category or not date:
        return render_template("expense_edit.html", expense=expense, error="All fields are required.")

    try:
        amount = float(amount)
        if amount <= 0:
            return render_template("expense_edit.html", expense=expense, error="Amount must be greater than 0.")
    except ValueError:
        return render_template("expense_edit.html", expense=expense, error="Please enter a valid amount.")

    # Update expense in database
    db_update_expense(id, amount, description, category, date)

    flash("Expense updated successfully!")
    return redirect(url_for("profile"))


@app.route("/expenses/<int:id>/delete", methods=["POST"])
def delete_expense(id):
    # Check authentication
    user_id = session.get("user_id")
    if not user_id:
        flash("Please sign in to delete an expense.")
        return redirect(url_for("login"))

    # Get expense and verify ownership
    expense = db_get_expense_by_id(id)
    if not expense:
        flash("Expense not found.")
        return redirect(url_for("profile"))

    if expense["user_id"] != user_id:
        flash("You don't have permission to delete this expense.")
        return redirect(url_for("profile"))

    # Delete expense from database
    db_delete_expense(id)

    flash("Expense deleted successfully!")
    return redirect(url_for("profile"))


if __name__ == "__main__":
    app.run(port=5001, debug=False)