# Spec: Profile Page Design

## Overview
A user profile page that displays account information including name, email, member since date, expense statistics (total count and total spent), and provides navigation to manage expenses. This page serves as the user's dashboard after logging in.

## Depends on
- Step 2: Registration (users table exists)
- Step 3: Login and Logout (authentication works, session management)

## Routes
- `GET /profile` — Display user profile with stats — logged-in only

## Database changes
No database changes required. Uses existing `get_user_by_id()` and `get_expense_summary()` functions from `database/db.py`.

## Templates
- **Create:** `templates/profile.html`
  - User info section: name, email, member since date
  - Stats section: expense count, total spent (in INR)
  - Navigation: link to add expense, link to logout
- **Modify:** `templates/base.html`
  - Add profile link to navigation when user is logged in

## Files to change
- `templates/base.html` — Add conditional profile link in nav

## Files to create
- `templates/profile.html` — Profile page template
- `static/css/profile.css` — Profile page styles

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
- Format large numbers with comma separators (e.g., ₹1,234.56)

## Definition of done
- [ ] GET /profile redirects to login if not authenticated
- [ ] Profile displays user name, email, and member since date
- [ ] Profile displays expense count
- [ ] Profile displays total spent in INR
- [ ] Profile has link to add expense page
- [ ] Profile has logout button
- [ ] Base.html shows profile link in nav when logged in
- [ ] All links use url_for()
- [ ] Page uses CSS variables for colors
- [ ] Large amounts formatted with commas