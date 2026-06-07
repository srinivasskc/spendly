# Spec: Registration

## Overview
User registration functionality that allows new users to create an account. Users provide name, email, and password. The password is securely hashed using werkzeug before storing in the database. On successful registration, users are redirected to the login page with a success message.

## Depends on
- Step 1: Database Setup (users table exists)

## Routes
- `GET /register` — Render registration form — public
- `POST /register` — Process registration form — public

## Database changes
No database changes required. The `users` table was created in Step 1.

## Templates
- **Modify:** `templates/register.html`
  - Add a registration form with fields: name, email, password, confirm password
  - Add form validation (client-side and server-side)
  - Display error messages for duplicate email, validation errors
  - Add success message display area

## Files to change
- `app.py` — Add POST handler for /register route
- `templates/register.html` — Add registration form

## Files to create
- None

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug.security.generate_password_hash
- Use CSS variables from base.html (tailwind classes) — never hardcode hex values
- All templates extend `base.html`
- Use url_for() for all internal links
- Store passwords using werkzeug hashing (not plain text)
- Validate email format and password minimum length
- Check for duplicate email before inserting

## Definition of done
- [ ] GET /register renders the registration form template
- [ ] POST /register with valid data creates a new user in the database
- [ ] Password is hashed before storing (use werkzeug)
- [ ] POST /register with duplicate email shows error message
- [ ] POST /register with invalid data shows appropriate error messages
- [ ] Successful registration redirects to /login with success flash message
- [ ] Form uses proper HTML5 validation (required, email type, minlength)
- [ ] All database queries use parameterized placeholders (?)