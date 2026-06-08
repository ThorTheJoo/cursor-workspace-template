#!/usr/bin/env python3
"""Convert Nett Pay List (.xls / .xlsx) to FNB Online Banking Payment CSV (SA)."""

from __future__ import annotations

import argparse
import csv
import re
import sys
from datetime import datetime
from pathlib import Path

try:
    import xlrd
except ImportError:
    xlrd = None

try:
    import openpyxl
except ImportError:
    openpyxl = None

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG = ROOT / "config" / "site.yaml"
INPUTS_ROOT = ROOT / "docs" / "_ai_context" / "inputs"
EMPLOYEE_CODE_RE = re.compile(r"^[A-Z]\d+")
BANKABLE_PAY_METHODS = {"ACB"}
VALID_ACCOUNT_TYPES = {"0", "1", "2", "3", "4", "6", "D", "F", "W"}

CSV_HEADER = [
    "RECIPIENT NAME", "RECIPIENT ACCOUNT", "RECIPIENT ACCOUNT TYPE", "BRANCHCODE",
    "AMOUNT", "OWN REFERENCE", "RECIPIENT REFERENCE",
    "EMAIL 1 NOTIFY", "EMAIL 1 ADDRESS", "EMAIL 1 SUBJECT",
    "EMAIL 2 NOTIFY", "EMAIL 2 ADDRESS", "EMAIL 2 SUBJECT",
    "EMAIL 3 NOTIFY", "EMAIL 3 ADDRESS", "EMAIL 3 SUBJECT",
    "EMAIL 4 NOTIFY", "EMAIL 4 ADDRESS", "EMAIL 4 SUBJECT",
    "EMAIL 5 NOTIFY", "EMAIL 5 ADDRESS", "EMAIL 5 SUBJECT",
    "FAX 1 NOTIFY", "FAX 1 CODE", "FAX 1 NUMBER", "FAX 1 SUBJECT",
    "FAX 2 NOTIFY", "FAX 2 CODE", "FAX 2 NUMBER", "FAX 2 SUBJECT",
    "SMS 1 NOTIFY", "SMS 1 CODE", "SMS 1 NUMBER",
    "SMS 2 NOTIFY", "SMS 2 CODE", "SMS 2 NUMBER",
]


def load_config(path: Path) -> dict:
    if yaml and path.exists():
        with path.open(encoding="utf-8") as f:
            return yaml.safe_load(f)
    return {
        "banking": {
            "nominated_account": "62848015857",
            "payroll": {
                "own_reference": "FuelRock Payroll",
                "recipient_reference_prefix": "Salary",
                "default_account_type": "2",
                "bank_account_types": {},
            },
        }
    }


def normalize_account(value) -> str:
    s = str(value).strip()
    if s.endswith(".0"):
        s = s[:-2]
    return re.sub(r"\D", "", s)


def parse_pay_date_from_rows(rows: list[tuple]) -> datetime | None:
    for row in rows[:5]:
        val = str(row[0] if row else "").strip()
        if isinstance(row[0], datetime):
            return row[0]
        for fmt in ("%Y/%m/%d", "%Y-%m-%d", "%d/%m/%Y"):
            try:
                return datetime.strptime(val, fmt)
            except ValueError:
                continue
    return None


def parse_employees_from_rows(rows: list[tuple]) -> list[dict]:
    employees: list[dict] = []
    for row in rows:
        if not row:
            continue
        code = str(row[0] or "").strip()
        if not EMPLOYEE_CODE_RE.match(code):
            continue
        try:
            net_pay = float(row[8] or 0)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"Invalid net pay for employee {code}: {row[8]}") from exc
        employees.append({
            "code": code,
            "name": str(row[1] or "").strip().upper(),
            "pay_method": str(row[3] or "").strip(),
            "bank": str(row[4] or "").strip(),
            "account": normalize_account(row[5]),
            "branch": normalize_account(row[7]),
            "net_pay": net_pay,
        })
    return employees


def split_bankable_employees(employees: list[dict]) -> tuple[list[dict], list[dict]]:
    bankable: list[dict] = []
    excluded: list[dict] = []
    for employee in employees:
        method = employee.get("pay_method", "").strip().upper()
        if method in BANKABLE_PAY_METHODS:
            bankable.append(employee)
        else:
            excluded.append({
                "code": employee.get("code", ""),
                "name": employee.get("name", ""),
                "pay_method": employee.get("pay_method", ""),
                "net_pay": employee.get("net_pay", 0.0),
                "reason": "Non-ACB pay method is excluded from bank payment CSV",
            })
    return bankable, excluded


def load_payroll_rows(path: Path) -> tuple[list[tuple], str]:
    suffix = path.suffix.lower()
    if suffix == ".xls":
        if not xlrd:
            raise RuntimeError("xlrd required for .xls files: pip install xlrd")
        wb = xlrd.open_workbook(str(path))
        sh = wb.sheet_by_index(0)
        rows = [tuple(sh.cell_value(r, c) for c in range(sh.ncols)) for r in range(sh.nrows)]
        return rows, "xls"
    if suffix == ".xlsx":
        if not openpyxl:
            raise RuntimeError("openpyxl required for .xlsx files")
        wb = openpyxl.load_workbook(str(path), read_only=True, data_only=True)
        sh = wb.active
        rows = [tuple(row) for row in sh.iter_rows(values_only=True)]
        wb.close()
        return rows, "xlsx"
    raise ValueError(f"Unsupported payroll format: {suffix}")


def calc_hash_total(own_account: str, recipient_accounts: list[str]) -> str:
    digit_sum = 0
    for acc in recipient_accounts:
        for ch in acc:
            if ch.isdigit():
                digit_sum += int(ch)
    own_digits = normalize_account(own_account)
    total = digit_sum + int(own_digits) if own_digits else digit_sum
    return str(total)[-12:].rjust(12, "0")


def account_type_for(bank: str, cfg: dict) -> str:
    payroll_cfg = cfg.get("banking", {}).get("payroll", {})
    mapping = payroll_cfg.get("bank_account_types", {})
    normalized = {str(k).strip().lower(): str(v).strip() for k, v in mapping.items()}
    return normalized.get(bank.strip().lower(), str(payroll_cfg.get("default_account_type", "2")))


def format_amount(amount: float) -> str:
    return f"{amount:.2f}"


def validate_employee_for_payment(emp: dict, cfg_stub: dict) -> None:
    code = emp.get("code", "")
    if not emp.get("name"):
        raise ValueError(f"Employee {code} has no recipient name")
    if not emp.get("account"):
        raise ValueError(f"Employee {code} has no recipient account")
    if len(emp["account"]) > 20:
        raise ValueError(f"Employee {code} account exceeds 20 characters")
    if len(emp.get("branch", "")) != 6:
        raise ValueError(f"Employee {code} branch code must be 6 digits")
    if emp.get("net_pay", 0) <= 0:
        raise ValueError(f"Employee {code} must have a positive net pay amount")
    account_type = account_type_for(emp.get("bank", ""), cfg_stub)
    if account_type not in VALID_ACCOUNT_TYPES:
        raise ValueError(f"Employee {code} has invalid account type {account_type}")


def build_payment_csv(
    employees: list[dict],
    pay_date: datetime,
    own_account: str,
    own_reference: str,
    recipient_ref_prefix: str,
    account_type_map: dict,
) -> list[list[str]]:
    accounts = [e["account"] for e in employees]
    hash_total = calc_hash_total(own_account, accounts)
    date_str = pay_date.strftime("%d-%m-%Y")

    rows: list[list[str]] = [
        ["BInSol - U ver 1.00"] + [""] * 35,
        [date_str] + [""] * 35,
        [own_account, hash_total] + [""] * 34,
        CSV_HEADER,
    ]

    cfg_stub = {"banking": {"payroll": {"bank_account_types": account_type_map, "default_account_type": "2"}}}
    ref_suffix = pay_date.strftime("%y%m%d")
    for emp in employees:
        validate_employee_for_payment(emp, cfg_stub)
        rows.append([
            emp["name"][:20],
            emp["account"],
            account_type_for(emp["bank"], cfg_stub),
            emp["branch"],
            format_amount(emp["net_pay"]),
            own_reference[:20],
            f"{recipient_ref_prefix} {ref_suffix}"[:20],
        ] + [""] * 28)

    return rows


def write_csv(rows: list[list[str]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for row in rows:
            padded = row + [""] * max(0, 36 - len(row))
            writer.writerow(padded[:36])


def convert(input_path: Path, output_path: Path, config_path: Path) -> dict:
    cfg = load_config(config_path)
    banking = cfg.get("banking", {})
    payroll_cfg = banking.get("payroll", {})

    rows, fmt = load_payroll_rows(input_path)
    pay_date = parse_pay_date_from_rows(rows) or datetime.now()
    all_employees = parse_employees_from_rows(rows)
    if not all_employees:
        raise ValueError(f"No employees found in {input_path}")
    employees, excluded_employees = split_bankable_employees(all_employees)
    if not employees:
        raise ValueError(f"No ACB employees found in {input_path}")

    csv_rows = build_payment_csv(
        employees=employees,
        pay_date=pay_date,
        own_account=normalize_account(banking.get("nominated_account", "")),
        own_reference=payroll_cfg.get("own_reference", "Payroll"),
        recipient_ref_prefix=payroll_cfg.get("recipient_reference_prefix", "Salary"),
        account_type_map=payroll_cfg.get("bank_account_types", {}),
    )
    write_csv(csv_rows, output_path)

    return {
        "source_file": input_path.name,
        "source_type": "payroll_system",
        "format": fmt,
        "pay_date": pay_date.strftime("%Y-%m-%d"),
        "employee_count": len(employees),
        "source_employee_count": len(all_employees),
        "excluded_employee_count": len(excluded_employees),
        "total_net_pay": round(sum(e["net_pay"] for e in employees), 2),
        "source_total_net_pay": round(sum(e["net_pay"] for e in all_employees), 2),
        "excluded_total_net_pay": round(sum(e["net_pay"] for e in excluded_employees), 2),
        "hash_total": csv_rows[2][1],
        "output": str(output_path),
        "employees": employees,
        "excluded_employees": excluded_employees,
    }


def find_payroll_files(directory: Path) -> list[Path]:
    files = list(directory.rglob("Nett Pay List*.xls")) + list(directory.rglob("Nett Pay List*.xlsx"))
    return sorted(
        {p.resolve() for p in files if not re.search(r"\s\(\d+\)", p.stem)},
        key=lambda p: p.name,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert Nett Pay List to Payment CSV")
    parser.add_argument("input", nargs="?", help="Path to Nett Pay List .xls/.xlsx")
    parser.add_argument("-o", "--output", help="Output CSV path")
    parser.add_argument("-c", "--config", default=str(DEFAULT_CONFIG))
    parser.add_argument("--all", action="store_true", help="Process all Nett Pay List files found")
    args = parser.parse_args()

    config_path = Path(args.config)

    if args.all:
        files = find_payroll_files(INPUTS_ROOT)
        if not files:
            files = find_payroll_files(INPUTS_ROOT / "Starter Docs")
        for f in files:
            stem = f.stem.replace("Nett Pay List - ", "").replace("Nett Pay List", "").strip(" -")
            out = ROOT / "reports" / "payroll" / f"Payment_{stem}.csv"
            result = convert(f, out, config_path)
            print(f"OK {f.name}: {result['employee_count']} employees, R {result['total_net_pay']:,.2f} -> {out.name}")
        return

    input_path = Path(args.input) if args.input else None
    if not input_path:
        candidates = find_payroll_files(INPUTS_ROOT)
        if not candidates:
            candidates = find_payroll_files(INPUTS_ROOT / "Starter Docs")
        input_path = max(candidates, key=lambda p: p.stat().st_mtime) if candidates else None

    if not input_path or not input_path.exists():
        print("No Nett Pay List file found.", file=sys.stderr)
        sys.exit(1)

    stem = input_path.stem.replace("Nett Pay List - ", "").replace("Nett Pay List", "").strip(" -")
    output_path = Path(args.output) if args.output else ROOT / "reports" / "payroll" / f"Payment_{stem}.csv"

    result = convert(input_path, output_path, config_path)
    print(f"Generated: {result['output']}")
    print(f"Employees: {result['employee_count']} | Total: R {result['total_net_pay']:,.2f}")
    print(f"Pay date: {result['pay_date']} | Hash total: {result['hash_total']}")


if __name__ == "__main__":
    main()
