from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from datetime import datetime
import os
import re

from database.db import get_db

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


@app.route("/login")
def login():
    return render_template("login.html")


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
    return "Logout — coming in Step 3"


@app.route("/profile")
def profile():
    return "Profile page — coming in Step 4"


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    app.run(port=5001, debug=False)