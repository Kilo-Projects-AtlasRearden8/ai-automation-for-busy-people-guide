# Bill Reminders

Never miss a due date. This automation reads a simple list of bills and tells
you which ones are coming up soon — perfect for low-energy days when paperwork
feels overwhelming.

## What it does

Reads `bills.json` and prints reminders for bills due within the next 7 days
(you can change the window). It shows:

- Bill name
- Due date
- Amount
- Days left
- A "PAID" or "DUE SOON" flag

## bills.json example

```json
[
  {
    "name": "Electricity",
    "due_date": "2026-11-05",
    "amount": 87.50,
    "paid": false
  },
  {
    "name": "Internet",
    "due_date": "2026-11-10",
    "amount": 65.00,
    "paid": true
  }
]
```

- `name` — what the bill is
- `due_date` — YYYY-MM-DD format
- `amount` — how much (optional)
- `paid` — true/false (optional, defaults to false)

## How to run

1. Copy `scripts/bill_reminders.py` and `bills.json` to your computer.
2. Edit `bills.json` with your own bills (no real secrets needed — just names
   and dates).
3. Run:

   ```bash
   python3 scripts/bill_reminders.py --bills bills.json
   ```

   Bills due soon show at the top. Paid bills are marked PAID.

## Options

- `--days` — how far ahead to look (default: 7)
- `--upcoming` — show only unpaid bills due soon

## No-code alternative

Use your phone's calendar or a free app like Google Calendar. Set a reminder
2 days before each bill is due. Paper works too: write due dates on a wall
calendar.

**Asdale Dynamics, LLC** — tested, local-first, no secrets. Education only;
this is not financial advice.
