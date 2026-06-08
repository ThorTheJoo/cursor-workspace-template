#!/usr/bin/env python3
"""Validate generated FNB Online Banking payment CSV files."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "payroll"))

from netpay_to_payment_csv import CSV_HEADER, VALID_ACCOUNT_TYPES, calc_hash_total, normalize_account


def read_csv(path: Path) -> list[list[str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.reader(f))


def validate_payment_csv(path: Path, own_account: str | None = None) -> dict[str, Any]:
    rows = read_csv(path)
    errors: list[str] = []

    if len(rows) < 5:
        errors.append("CSV must contain preamble, header, and at least one recipient row")
    for idx, row in enumerate(rows, start=1):
        if len(row) != 36:
            errors.append(f"Row {idx} has {len(row)} columns; expected 36")

    if rows and rows[0][0] != "BInSol - U ver 1.00":
        errors.append("Row 1 must start with BInSol - U ver 1.00")
    if len(rows) > 1 and not re.match(r"^\d{2}-\d{2}-\d{4}$", rows[1][0]):
        errors.append("Row 2 must contain payment date as DD-MM-YYYY")
    if len(rows) > 2:
        csv_own_account = normalize_account(rows[2][0])
        expected_own_account = normalize_account(own_account or rows[2][0])
        if not csv_own_account:
            errors.append("Row 3 own account is required")
        if expected_own_account and csv_own_account != expected_own_account:
            errors.append("Row 3 own account does not match expected account")
        if not re.match(r"^\d{12}$", rows[2][1]):
            errors.append("Row 3 hash total must be 12 digits")
    if len(rows) > 3 and rows[3] != CSV_HEADER:
        errors.append("Row 4 header does not match the FNB payment CSV template")

    total = 0.0
    recipient_accounts: list[str] = []
    recipient_count = 0
    for row_number, row in enumerate(rows[4:], start=5):
        if not any(cell.strip() for cell in row):
            continue
        recipient_count += 1
        name = row[0].strip()
        account = normalize_account(row[1])
        account_type = row[2].strip()
        branch = normalize_account(row[3])
        amount_raw = row[4].strip()
        own_ref = row[5].strip()
        recipient_ref = row[6].strip()

        if not name or len(name) > 20:
            errors.append(f"Row {row_number} recipient name must be 1-20 characters")
        if not account or len(account) > 20:
            errors.append(f"Row {row_number} recipient account must be 1-20 digits")
        if account_type not in VALID_ACCOUNT_TYPES:
            errors.append(f"Row {row_number} account type {account_type!r} is not allowed")
        if len(branch) != 6:
            errors.append(f"Row {row_number} branch code must be 6 digits")
        if len(own_ref) > 20 or len(recipient_ref) > 20:
            errors.append(f"Row {row_number} references must be <= 20 characters")
        if not re.match(r"^\d{1,8}(\.\d{1,2})?$", amount_raw):
            errors.append(f"Row {row_number} amount is not a valid FNB amount")
            continue
        amount = float(amount_raw)
        if amount <= 0:
            errors.append(f"Row {row_number} amount must be positive")
        total += amount
        recipient_accounts.append(account)

    if len(rows) > 2:
        expected_hash = calc_hash_total(rows[2][0], recipient_accounts)
        if rows[2][1] != expected_hash:
            errors.append(f"Row 3 hash total {rows[2][1]} does not match recomputed {expected_hash}")

    return {
        "file": str(path),
        "valid": not errors,
        "errors": errors,
        "recipient_count": recipient_count,
        "total_amount": round(total, 2),
        "hash_total": rows[2][1] if len(rows) > 2 else "",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate an FNB payment CSV")
    parser.add_argument("csv_path", help="Path to Payment_*.csv")
    parser.add_argument("--own-account", help="Expected nominated account")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    args = parser.parse_args()

    result = validate_payment_csv(Path(args.csv_path), args.own_account)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        status = "PASS" if result["valid"] else "FAIL"
        print(f"{status} {result['file']}: {result['recipient_count']} rows, R {result['total_amount']:,.2f}")
        for error in result["errors"]:
            print(f"ERROR: {error}")
    if not result["valid"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
