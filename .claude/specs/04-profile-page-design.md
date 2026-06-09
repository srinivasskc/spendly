# Spec: Profile Page Design

## Overview
A user profile page that displays the logged-in user's account information including their name, email, member since date, and expense summary statistics. Users can view their profile and update their name. This is Step 4 of the Spendly roadmap.

## Depends on
- Step 2: Registration (users table exists, users can register)
- Step 3: Login and Logout (session management works, user_id stored in session)

## Routes
- `GET /profile` — Display user profile — logged-in only

## Database changes
No new tables or columns required. The existing `users` table has all necessary fields (id, name, email, created_at).

## Templates
- **Create:** `templates/profile.html` — User profile page with:
  - User name and email display
  - Member since date formatted nicely
  - Expense summary (total expenses count, total amount spent)
  - Account details display (read-only)

## Files to change
- `app.py` — Implement GET /profile route to fetch user data and render template

## Files to create
- `templates/profile.html` — Profile page template

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Use CSS variables from base.html — never hardcode hex values
- All templates extend `base.html`
- Use url_for() for all internal links and form actions
- Profile page requires logged-in user (check session.get('user_id'))
- Redirect to login if user not authenticated
- Use werkzeug for password hashing (already imported in app.py)

## Definition of done
- [ ] GET /profile redirects to login when user is not authenticated
- [ ] GET /profile shows user's name, email, and member since date
- [ ] GET /profile shows expense summary (total count, total amount)
- [ ] GET /profile shows account details (read-only display)
- [ ] Profile page extends base.html
- [ ] Profile page uses url_for() for all links
- [ ] Profile page uses CSS variables from base.html theme
- [ ] Navbar shows "Profile" link when user is logged in (already done in base.html)