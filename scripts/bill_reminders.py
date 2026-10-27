#!/usr/bin/env python3
"""Bill reminders: shows which bills are due soon.

Reads a bills.json file and prints upcoming bills. Nothing is modified.
"""

import argparse
import json
import sys
from datetime import date, timedelta
from pathlib import Path


def load_bills(path: Path):
    with path.open("r", encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, list):
        raise ValueError("bills.json must contain a list of bills")
    return data


def parse_bill(item):
    if not isinstance(item, dict):
        raise ValueError("each bill must be an object")
    name = item.get("name", "Unnamed bill")
    due_str = item.get("due_date")
    if not due_str:
        raise ValueError(f"bill '{name}' is missing due_date")
    due = date.fromisoformat(due_str)
    amount = item.get("amount")
    paid = bool(item.get("paid", False))
    return {"name": name, "due": due, "amount": amount, "paid": paid}


def run(bills_path: Path, days: int, upcoming_only: bool) -> int:
    try:
        raw = load_bills(bills_path)
    except FileNotFoundError:
        print(f"Error: bills file not found: {bills_path}")
        return 1
    except (json.JSONDecodeError, ValueError) as exc:
        print(f"Error: invalid bills file: {exc}")
        return 1

    bills = []
    for item in raw:
        try:
            bills.append(parse_bill(item))
        except ValueError as exc:
            print(f"Warning: skipping invalid bill: {exc}")
            continue

    today = date.today()
    cutoff = today + timedelta(days=days)

    upcoming = [
        b for b in bills
        if today <= b["due"] <= cutoff and not b["paid"]
    ]
    upcoming.sort(key=lambda b: b["due"])

    if upcoming_only and not upcoming:
        print("No unpaid bills due soon.")
        return 0

    print(f"Bill reminders (next {days} days, from {today.isoformat()})")
    print("=" * 50)

    if not upcoming:
        print("No bills due soon. ")
        return 0

    for bill in upcoming:
        days_left = (bill["due"] - today).days
        amount_str = f"${bill['amount']:.2f}" if bill["amount"] is not None else "?"
        flag = "DUE TODAY" if days_left == 0 else f"due in {days_left} day(s)"
        print(f"  {bill['name']}")
        print(f"    Due: {bill['due'].isoformat()}  ({flag})")
        print(f"    Amount: {amount_str}")
        print()

    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Show bills due soon from a bills.json file."
    )
    parser.add_argument(
        "--bills",
        type=Path,
        default=Path("bills.json"),
        help="Path to bills.json (default: bills.json)",
    )
    parser.add_argument(
        "--days",
        type=int,
        default=7,
        help="Look ahead this many days (default: 7)",
    )
    parser.add_argument(
        "--upcoming",
        action="store_true",
        help="Show only unpaid bills due soon",
    )
    args = parser.parse_args(argv)
    return run(args.bills, args.days, args.upcoming)


if __name__ == "__main__":
    sys.exit(main())
