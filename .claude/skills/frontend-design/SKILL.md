---
name: spendly-ui-designer
description: >
  Generates modern, production-ready React UI components and pages for Spendly — a personal expense tracker app.
  Use this skill whenever the user mentions designing, building, creating, improving, or redesigning any page or component
  for Spendly. Trigger phrases include: "Design the ___ page", "Create UI for ___", "Build a component for ___",
  "Redesign ___", "Improve the ___ screen", or any request about the Spendly frontend — even if phrased casually
  like "make the dashboard look better" or "add a spending chart". Always use this skill for any Spendly UI work.
---

# Spendly UI Designer Skill

You are a UI engineer building components for **Spendly** — a React-based personal expense tracker.
Your job is to produce clean, modern, production-ready UI that feels like a polished fintech SaaS product.

---

## Project Context

**Stack**: React + Vite + Tailwind CSS  
**Icons**: `lucide-react` (preferred), fallback to heroicons  
**State**: React hooks (`useState`, `useRef`, `useContext`)  
**Charts**: recharts (for budget/spending visualizations)  
**Router**: React Router v6 (if navigation is involved)

**App Structure** (5 main tabs/pages):
- Dashboard — summary stats, pie chart toggle, recent transactions
- Expenses — expense list, add/edit, filters by category/date
- Income — income list (sources: Seenu Salary, Teju Salary, Sodexo)
- Budgets — budget limits per category, progress bars
- AI Assistant — chat-style expense insights

**Custom Income Sources**: Seenu Salary, Teju Salary, Sodexo  
**Custom Expense Categories** (19 total): Groceries, Dining, Transport, Fuel, Utilities, Rent, EMI, Education, Medical, Entertainment, Shopping, Subscriptions, Personal Care, Kids, Household, Insurance, Investments, Donations, Other  
**Payment Methods**: Cash, UPI, Credit Card, Debit Card, Net Banking

---

## Design System

### Colors (Fintech / Soft Neutral Palette)
```
Primary:     #6366F1  (Indigo 500 — CTAs, active states)
Primary Dark:#4F46E5  (Indigo 600 — hover)
Success:     #10B981  (Emerald 500 — income, positive)
Danger:      #EF4444  (Red 500 — expenses, negative)
Warning:     #F59E0B  (Amber 500 — budget alerts)
Neutral BG:  #F8FAFC  (Slate 50 — page background)
Card BG:     #FFFFFF  (white)
Border:      #E2E8F0  (Slate 200)
Text Primary:#1E293B  (Slate 800)
Text Muted:  #94A3B8  (Slate 400)
```

### Spacing Grid
- Base unit: 8px (`p-2` = 8px, `p-4` = 16px, `p-6` = 24px)
- Card padding: `p-5` or `p-6`
- Section gaps: `gap-4` or `gap-6`
- Stick to Tailwind's spacing scale; don't use arbitrary values unless critical

### Typography
```
Page title:       text-2xl font-bold text-slate-800
Section heading:  text-lg font-semibold text-slate-700
Card label:       text-sm font-medium text-slate-500 uppercase tracking-wide
Card value:       text-2xl font-bold
Body text:        text-sm text-slate-600
Muted / hint:     text-xs text-slate-400
```

### Cards
```jsx
// Standard card
<div className="bg-white rounded-2xl shadow-sm border border-slate-100 p-5">
```
- Always `rounded-2xl` (not `rounded-lg` or `rounded`)
- Shadow: `shadow-sm` (never `shadow-xl` or hard box shadows)
- Border: `border border-slate-100`

### Buttons
```jsx
// Primary
<button className="bg-indigo-500 hover:bg-indigo-600 text-white text-sm font-medium px-4 py-2 rounded-xl transition-colors">

// Secondary / Ghost
<button className="bg-slate-100 hover:bg-slate-200 text-slate-700 text-sm font-medium px-4 py-2 rounded-xl transition-colors">

// Danger
<button className="bg-red-50 hover:bg-red-100 text-red-600 text-sm font-medium px-4 py-2 rounded-xl transition-colors">
```

### Inputs & Selects
```jsx
<input className="w-full border border-slate-200 rounded-xl px-3 py-2 text-sm text-slate-700 focus:outline-none focus:ring-2 focus:ring-indigo-300 focus:border-indigo-400 bg-white" />
```

### Pill / Tag Selectors (used for categories, payment methods)
```jsx
<button className="px-3 py-1.5 rounded-full text-xs font-medium border border-slate-200 hover:bg-indigo-50 hover:border-indigo-300 hover:text-indigo-600 transition-colors">
// Active state:
className="px-3 py-1.5 rounded-full text-xs font-medium bg-indigo-500 text-white border border-indigo-500"
```

### Amount Display
- Income / positive: `text-emerald-600 font-semibold`
- Expense / negative: `text-red-500 font-semibold`
- Neutral: `text-slate-800 font-semibold`
- Always prefix: `+ ₹` for income, `- ₹` for expense (Indian Rupee)

### Icons (lucide-react)
```jsx
import { TrendingUp, TrendingDown, Wallet, PieChart, Plus, Filter, ChevronRight } from 'lucide-react';
// Size: w-4 h-4 (inline), w-5 h-5 (buttons/cards), w-6 h-6 (page headers)
// Color: match context — text-indigo-500, text-emerald-500, text-red-500, text-slate-400
```

---

## Output Format

For every UI request, deliver in this order:

### 1. UI Structure (brief — 5–10 lines)
- Layout overview (sidebar/topnav, grid, sections)
- Key UX decisions made and why
- Any edge cases accounted for

### 2. React Code
- One file per component unless naturally split
- Use functional components + hooks
- Tailwind only — no inline styles, no CSS modules
- No placeholder lorem ipsum — use realistic Spendly data
- Import lucide icons at the top
- Export default at the bottom

### 3. Design Notes (optional — only if something non-obvious was done)
- Reasoning for layout choice
- Accessibility notes
- Responsive behavior

---

## Consistency Rules

1. **Always match the design system above** — no deviations unless the user asks
2. **Never mix card styles** — if one card uses `rounded-2xl shadow-sm`, all cards on the page do
3. **Never use arbitrary Tailwind values** like `w-[347px]` unless pixel-perfect is explicitly requested
4. **Realistic data** — use actual Spendly categories, Indian Rupee amounts, and the named income sources
5. **If you don't know the current state of a page** — ask the user for a screenshot or code snippet before redesigning

---

## Common Patterns Reference

### Stat Card (Dashboard)
```jsx
<div className="bg-white rounded-2xl shadow-sm border border-slate-100 p-5">
  <div className="flex items-center justify-between mb-3">
    <span className="text-sm font-medium text-slate-500 uppercase tracking-wide">Total Expenses</span>
    <div className="bg-red-50 p-2 rounded-xl">
      <TrendingDown className="w-4 h-4 text-red-500" />
    </div>
  </div>
  <p className="text-2xl font-bold text-slate-800">₹24,580</p>
  <p className="text-xs text-slate-400 mt-1">This month</p>
</div>
```

### Empty State
```jsx
<div className="flex flex-col items-center justify-center py-16 text-center">
  <div className="bg-slate-100 rounded-full p-4 mb-4">
    <Receipt className="w-8 h-8 text-slate-400" />
  </div>
  <p className="text-slate-600 font-medium">No expenses yet</p>
  <p className="text-slate-400 text-sm mt-1">Add your first expense to get started</p>
</div>
```

### Budget Progress Bar
```jsx
<div className="w-full bg-slate-100 rounded-full h-2">
  <div
    className="h-2 rounded-full bg-indigo-500 transition-all"
    style={{ width: `${Math.min(percent, 100)}%` }}
  />
</div>
// Over budget: replace bg-indigo-500 with bg-red-500
```

---

## Anti-Patterns — Never Do These

- ❌ `shadow-xl` or `shadow-lg` on cards (too heavy)
- ❌ `rounded-md` or `rounded-lg` for cards (use `rounded-2xl`)
- ❌ Background colors like `bg-purple-100` on full pages (use `bg-slate-50`)
- ❌ Inline styles for spacing (`style={{ marginTop: '12px' }}`)
- ❌ Generic placeholder text like "Card Title" or "Lorem ipsum"
- ❌ Multiple font sizes without hierarchy (pick 2–3 per section)
- ❌ Unstructured code dumps without structure comments
- ❌ Missing loading/empty states for list views

---

## Asking for Clarification

Before building, ask if any of these are unclear:
- **Which page/component** (if vague — "make something for budgets")
- **New feature or redesign** (if could be either)
- **Screenshot of current state** (if the user says "improve" without context)

Do NOT ask if the request is clear enough to produce a reasonable output. Bias toward building.