# Spec: Backend Routes for Profile Page

## Overview
This step documents and completes the backend routes required for the Profile page to function. The Profile page serves as the user's dashboard after login, displaying account information, expense statistics, and recent transactions.

## Depends on
- Step 2: Registration (users table exists)
- Step 3: Login and Logout (authentication works, session management)
- Step 4: Profile Page Design (template exists)

## Routes

### Existing Route — Already Implemented
- `GET /profile` — Display user profile with stats — logged-in only

This route is already implemented in `app.py` (lines 138-170):
1. Checks authentication via session
2. Fetches user data using `get_user_by_id()`
3. Fetches expense summary using `get_expense_summary()`
4. Fetches recent expenses using `get_recent_expenses()`
5. Renders `profile.html` with all required data

### No New Routes Required
The profile backend route is already complete.

## Database changes
No database changes required. Uses existing functions from `database/db.py`:
- `get_user_by_id(user_id)` — retrieves user details
- `get_expense_summary(user_id)` — returns count and total
- `get_recent_expenses(user_id, limit)` — returns recent transactions

## Templates
No new templates required. `templates/profile.html` already exists and uses:
- `user.name` — User's name
- `user.email` — User's email
- `member_since` — Formatted date (e.g., "June 2026")
- `expense_count` — Total number of expenses
- `total_spent` — Total amount in INR
- `recent_expenses` — List of recent expense transactions

## Files to change
None — all files already exist and are properly connected.

## Files to create
None.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Use url_for() for all internal links
- Display currency in INR (use ₹ symbol)

## Definition of done
- [x] GET /profile redirects to login if not authenticated
- [x] Profile displays user name, email, and member since date
- [x] Profile displays expense count
- [x] Profile displays total spent in INR
- [x] Profile shows recent transactions
- [x] Profile has link to add expense page
- [x] Profile has logout button
- [x] All links use url_for()
- [x] Page uses CSS variables for colors
- [x] Large amounts formatted with commas

## Notes
**This step is already complete.** The profile backend route was implemented as part of Step 4 (Profile Page Design). The CLAUDE.md file incorrectly lists `GET /profile` as a stub — it should be marked as implemented.