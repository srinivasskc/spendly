# Spec: Date Filter in Profile Page

## Overview
This feature adds date filtering capability to the Profile page, allowing users to filter their expenses by a date range. Users can select a start date and/or end date to view expenses within that period. The filter applies to both the displayed expenses list and the total spent calculation.

## Depends on
- Step 2: Registration (users table exists)
- Step 3: Login and Logout (authentication works, session management)
- Step 4: Profile Page Design (profile page exists)
- Step 5: Backend Routes for Profile Page (profile route works)

## Routes
- `GET /profile` — Display user profile with optional date filtering — logged-in only

**Query Parameters:**
- `start_date` — Optional filter for expenses from this date (YYYY-MM-DD format)
- `end_date` — Optional filter for expenses until this date (YYYY-MM-DD format)

The existing route will be enhanced to accept query parameters.

## Database changes
- Add new function `get_filtered_expenses(user_id, start_date=None, end_date=None, limit=None)` to retrieve expenses within a date range
- Add new function `get_expense_summary_filtered(user_id, start_date=None, end_date=None)` to calculate totals for filtered results

No new tables or columns needed.

## Templates
### Modify
- `templates/profile.html` — Add date filter form with start date and end date inputs above the transactions list

## Files to change
- `database/db.py` — Add new filtered expense functions
- `app.py` — Modify profile route to handle date filter query parameters
- `templates/profile.html` — Add date filter UI
- `static/css/profile.css` — Add styles for date filter form

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
- Date format for input: YYYY-MM-DD (HTML date input)
- Display format for dates in UI: DD MMM YYYY (e.g., "15 Jul 2026")
- If only start_date provided: show expenses from that date onwards
- If only end_date provided: show expenses until that date
- If both provided: show expenses within the date range
- If neither provided: show all expenses (or recent 5 by default)

## Definition of done
- [ ] Profile page has date filter form with start and end date inputs
- [ ] Date filter form uses GET method with query parameters
- [ ] Filtering by start_date shows expenses from that date onwards
- [ ] Filtering by end_date shows expenses until that date
- [ ] Filtering by both start and end date shows expenses within range
- [ ] Total spent updates to reflect filtered results
- [ ] Expense count updates to reflect filtered results
- [ ] Dates display in readable format (DD MMM YYYY)
- [ ] Clear filter button resets to show all/recent expenses
- [ ] All links use url_for()
- [ ] Page uses CSS variables for colors