# Spec: Login and Logout

## Overview
User login and logout functionality that allows registered users to authenticate and access their account. Login verifies email and password credentials, then starts a session. Logout clears the session and redirects to the landing page.

## Depends on
- Step 2: Registration (users table exists, users can register)

## Routes
- `POST /login` — Process login credentials — public
- `GET /logout` — Clear session and redirect — logged-in only

## Database changes
No database changes required.

## Templates
- **Modify:** `templates/login.html`
  - Add flash message display for success messages
  - Form action uses url_for('login') instead of hardcoded /login

## Files to change
- `app.py` — Add POST handler for /login, implement /logout
- `database/db.py` — Add get_user_by_email function and password verification helper
- `templates/login.html` — Update form action to use url_for()

## Files to create
- None

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords verified with werkzeug.security.check_password_hash
- Use Flask sessions for authentication (store user_id in session)
- Use CSS variables from base.html — never hardcode hex values
- All templates extend `base.html`
- Use url_for() for all internal links and form actions

## Definition of done
- [ ] POST /login with valid credentials redirects to profile or landing page
- [ ] POST /login with invalid credentials shows error message
- [ ] POST /login with non-existent email shows error message
- [ ] GET /logout clears session and redirects to landing page
- [ ] Login form uses url_for() for action
- [ ] Successful login shows flash message
- [ ] Database queries use parameterized placeholders (?)
- [ ] Password verification uses werkzeug check_password_hash