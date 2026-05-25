#!/usr/bin/env python3
"""Parse ENGEN POS fixed-width TXT exports into canonical JSON."""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class FuelGradeEod:
    grade_id: str
    description: str
    amount: float
    pump_volume: float
    tank_volume: float
    variance_litres: float


@dataclass
class CategorySales:
    category: str
    qty_sold: float
    cost_of_sales: float
    sales_value: float
    tax: float
    total_sales: float
    gp_amount: float
    gp_percent: float


@dataclass
class CashierException:
    cashier: str
    nett_takings: float
    void_qty: int
    void_amount: float


@dataclass
class DayEndReport:
    source_file: str
    site_name: str
    batch_number: int
    batch_date: str
    report_generated: str
    shop_total_incl: float = 0.0
    fuel_total: float = 0.0
    combined_total: float = 0.0
    shop_gp_percent: float = 0.0
    fuel_gp_percent: float = 0.0
    nett_takings: float = 0.0
    cash_variance: float = 0.0
    fuel_customers: int = 0
    shop_customers: int = 0
    fuel_volume: float = 0.0
    fuel_grades: list[FuelGradeEod] = field(default_factory=list)
    top_categories: list[CategorySales] = field(default_factory=list)
    cashiers: list[CashierException] = field(default_factory=list)
    payouts: float = 0.0
    mtd_fuel_variance_pct: dict[str, float] = field(default_factory=dict)


def read_text(path: Path) -> str:
    for enc in ("utf-8", "cp1252", "latin-1"):
        try:
            return path.read_text(encoding=enc)
        except UnicodeDecodeError:
            continue
    return path.read_text(encoding="utf-8", errors="replace")


def parse_money(s: str) -> float:
    s = s.strip().replace(",", "")
    if not s or s == "-":
        return 0.0
    return float(s)


def parse_day_end(path: Path) -> DayEndReport:
    text = read_text(path)
    site_match = re.search(r"^(ENGEN[^\n]+)", text, re.M)
    gen_match = re.search(r"(ENGEN[^\n]+)\s+(\d{2}/\d{2}/\d{4}\s+\d{2}:\d{2})", text)
    batch_match = re.search(r"Batch Number\s*:\s*(\d+)", text)
    date_match = re.search(r"Batch Date\s*:\s*(\d{2}/\d{2}/\d{4})", text)

    site_raw = site_match.group(1).strip() if site_match else ""
    if gen_match:
        site_raw = gen_match.group(1).strip()

    report = DayEndReport(
        source_file=path.name,
        site_name=site_raw,
        batch_number=int(batch_match.group(1)) if batch_match else 0,
        batch_date=date_match.group(1) if date_match else "",
        report_generated=gen_match.group(2) if gen_match else "",
    )

    # Grand total line (combined shop+fuel)
    grand = re.search(
        r"(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+100\.00",
        text,
    )
    if grand:
        report.combined_total = parse_money(grand.group(5))
        report.shop_gp_percent = parse_money(grand.group(7))

    fuel_line = re.search(
        r"FUEL\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)",
        text,
    )
    if fuel_line:
        report.fuel_total = parse_money(fuel_line.group(5))
        report.fuel_volume = parse_money(fuel_line.group(1))
        report.fuel_gp_percent = parse_money(fuel_line.group(7))

    shop_block = re.search(
        r"^\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s*\n\s*\nFUEL",
        text,
        re.M,
    )
    if shop_block:
        report.shop_total_incl = parse_money(shop_block.group(5))

    nett = re.search(r"Nett Takings\s+(\d+\.\d+)", text)
    if nett:
        report.nett_takings = parse_money(nett.group(1))

    payouts = re.search(r"Payouts\s+-?(\d+\.\d+)", text)
    if payouts:
        report.payouts = parse_money(payouts.group(1))

    var = re.search(r"183824\.80\s+183805\.24\s+(\d+\.\d+)", text)
    if not var:
        var = re.search(
            r"(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s*\n-+\s*\nEOS",
            text,
        )
        if var:
            report.cash_variance = parse_money(var.group(8))
    else:
        report.cash_variance = parse_money(var.group(1))

    # Fuel EOD short — scoped section only
    eod_short = text
    start = text.find("Fuel Sales Control - EOD Short")
    end = text.find("Gross Profit Analysis", start if start >= 0 else 0)
    if start >= 0:
        eod_short = text[start:end if end > start else start + 2500]
    for m in re.finditer(
        r"^(\d{2})\s+(UNLEADED \d+|DSL \d+PPM)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(-?\d+\.\d+)",
        eod_short,
        re.M,
    ):
        report.fuel_grades.append(FuelGradeEod(
            grade_id=m.group(1),
            description=m.group(2).strip(),
            amount=parse_money(m.group(3)),
            pump_volume=parse_money(m.group(4)),
            tank_volume=parse_money(m.group(5)),
            variance_litres=parse_money(m.group(6)),
        ))

    # MTD fuel variance %
    for m in re.finditer(
        r"MONTHLY TOTALS:.*?VARIANCE PERCENTAGE\s+(\d+\.\d+)\s+%",
        text,
        re.S,
    ):
        pass
    for grade_id, desc in [("01", "UL93"), ("02", "UL95"), ("03", "DSL")]:
        block = re.search(
            rf"Grade ID\s*:\s*{grade_id}.*?VARIANCE PERCENTAGE\s+(\d+\.\d+)\s+%",
            text,
            re.S,
        )
        if block:
            report.mtd_fuel_variance_pct[desc] = parse_money(block.group(1))

    fuel_cust = re.search(r"Number of fuel customers\s+(\d+\.\d+)", text)
    shop_cust = re.search(r"Number Of Shop Customers\s+(\d+\.\d+)", text)
    if fuel_cust:
        report.fuel_customers = int(parse_money(fuel_cust.group(1)))
    if shop_cust:
        report.shop_customers = int(parse_money(shop_cust.group(1)))

    # Top categories (exclude FUEL/LUBES totals)
    for m in re.finditer(
        r"^(BAKERY|BAKPRE|BARIST|BEV|CH|CON|DAIRY|TOBACC|TOBCIG|SNK|FUEL|LUBES|[A-Z][A-Z0-9 ]{2,8})\s+"
        r"(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)",
        text,
        re.M,
    ):
        cat = m.group(1).strip()
        if cat in ("FUEL", "LUBES", "---"):
            continue
        report.top_categories.append(CategorySales(
            category=cat,
            qty_sold=parse_money(m.group(2)),
            cost_of_sales=parse_money(m.group(3)),
            sales_value=parse_money(m.group(4)),
            tax=parse_money(m.group(5)),
            total_sales=parse_money(m.group(6)),
            gp_amount=parse_money(m.group(7)),
            gp_percent=parse_money(m.group(8)),
        ))

    # Cashier exceptions
    for m in re.finditer(
        r"^(CAROLI|OPT|SIA|TUMELO|SPHA|CONNY|DINA|PULEDI|B300)\s+(\d+\.\d+)\s+(\d+)\s+(\d+\.\d+)",
        text,
        re.M,
    ):
        report.cashiers.append(CashierException(
            cashier=m.group(1),
            nett_takings=parse_money(m.group(2)),
            void_qty=int(m.group(3)),
            void_amount=parse_money(m.group(4)),
        ))

    return report


def parse_month_end(path: Path) -> dict[str, Any]:
    text = read_text(path)
    month_label = re.search(r"(\d{2}/\d{2}/\d{4}).*?-\s*(\w+\s+\d{4})", text)
    nett = re.search(r"Nett Takings\s+(\d[\d,\.]+)", text)
    cash_var = re.search(
        r"Total BANKING.*?(\-?\d+\.\d+)\s*\n\n\*\*\* EFT",
        text,
        re.S,
    )
    fuel_mtd = re.search(
        r"FUEL\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)",
        text,
    )
    combined = re.search(
        r"(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+100\.00",
        text,
    )
    fuel_var = re.search(
        r"(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\-?\d+\.\d+)\s+(\-?\d+\.\d+)\s*\n(?:<|\Z)",
        text[text.find("Fuel Sales Control - MTD Short"):] if "Fuel Sales Control - MTD Short" in text else text,
    )
    return {
        "source_file": path.name,
        "period": month_label.group(2) if month_label else "",
        "month_end_date": month_label.group(1) if month_label else "",
        "nett_takings": parse_money(nett.group(1)) if nett else 0,
        "cash_variance_banking": parse_money(cash_var.group(1)) if cash_var else 0,
        "fuel_volume": parse_money(fuel_mtd.group(1)) if fuel_mtd else 0,
        "fuel_sales": parse_money(fuel_mtd.group(5)) if fuel_mtd else 0,
        "combined_sales": parse_money(combined.group(5)) if combined else 0,
        "combined_gp_pct": parse_money(combined.group(7)) if combined else 0,
        "fuel_mtd_variance_litres": parse_money(fuel_var.group(4)) if fuel_var else 0,
        "fuel_mtd_variance_pct": parse_money(fuel_var.group(5)) if fuel_var else 0,
    }


def parse_eft_pending(path: Path) -> dict[str, Any]:
    text = read_text(path)
    total = re.search(r"Total\s*:\s*(\d+\.\d+)", text)
    forecourt = re.search(r"\*\*\* Forecourt\s*\n(.*?)\\n\\n\\*\\*\\* Retail", text, re.S)
    items = len(re.findall(r"\d{6}\s+\d{2}/\d{2}/\d{4}", text))
    return {
        "source_file": path.name,
        "pending_total": parse_money(total.group(1)) if total else 0,
        "transaction_count": items,
    }


def parse_eft_batch_summary(path: Path) -> dict[str, Any]:
    text = read_text(path)
    date = re.search(r"From EFT Batch Date\s+(\d{2}/\d{2}/\d{4})", text)
    total = re.search(r"Total For EFT Batch Date.*?(\d+)\s+(\d+\.\d+)", text, re.S)
    forecourt = re.search(r"\*\*\* Forecourt\s*\n.*?(\d+)\s+(\d+\.\d+)", text, re.S)
    retail = re.search(r"\*\*\* Retail\s*\n.*?(\d+)\s+(\d+\.\d+)", text, re.S)
    return {
        "source_file": path.name,
        "batch_date": date.group(1) if date else "",
        "total_trx": int(total.group(1)) if total else 0,
        "total_amount": parse_money(total.group(2)) if total else 0,
        "forecourt_amount": parse_money(forecourt.group(2)) if forecourt else 0,
        "retail_amount": parse_money(retail.group(2)) if retail else 0,
    }


def _parse_cash_variance_amounts(line: str) -> list[float] | None:
    values = re.findall(r"-?\d[\d,]*\.\d{2}", line)
    if len(values) != 7:
        return None
    return [parse_money(value) for value in values]


def parse_cash_variance_by_cashier(path: Path) -> dict[str, Any]:
    text = read_text(path)
    batch = re.search(r"Batch No\s*:\s*(\d+)", text)
    date = re.search(r"Batch Date\s*:\s*(\d{2}/\d{2}/\d{4})", text)
    if not batch or not date:
        raise ValueError(f"Cash variance report missing batch metadata: {path}")

    blocks = re.finditer(
        r"Till\s*:\s*(?P<till>\d+)\s*\n"
        r"Cashier\s*:\s*(?P<cashier>[^\n]+)\n"
        r"Start Date\s*:\s*(?P<start_date>\d{2}/\d{2}/\d{4})\n"
        r"Start Time\s*:\s*(?P<start_time>\d{2}:\d{2}:\d{2})\n"
        r"End Date\s*:\s*(?P<end_date>\d{2}/\d{2}/\d{4})\n"
        r"End Time\s*:\s*(?P<end_time>\d{2}:\d{2}:\d{2})\n"
        r"Shift No\s*:\s*(?P<shift_no>\d+)\n"
        r"Batch Date\s*:\s*(?P<batch_date>\d{2}/\d{2}/\d{4})\n"
        r"Batch No\s*:\s*(?P<batch_no>\d+)\n"
        r"-+\n(?P<body>.*?)(?=\n-+\nTill\s*:|\Z)",
        text,
        re.S,
    )

    shifts: list[dict[str, Any]] = []
    cashier_totals: dict[str, dict[str, Any]] = {}
    for block in blocks:
        body = block.group("body")
        total_match = re.search(r"^Total OTHER\s+.*$", body, re.M)
        if not total_match:
            continue
        total_values = _parse_cash_variance_amounts(total_match.group(0))
        if not total_values:
            continue

        cash_match = re.search(r"^CASH\s+.*$", body, re.M)
        cash_values = _parse_cash_variance_amounts(cash_match.group(0)) if cash_match else None
        cashier = block.group("cashier").strip()
        total_actual = total_values[4]
        total_theoretical = total_values[5]
        total_variance = total_values[6]
        cash_actual = cash_values[4] if cash_values else 0.0
        cash_theoretical = cash_values[5] if cash_values else 0.0
        cash_variance = cash_values[6] if cash_values else 0.0

        shifts.append({
            "till": int(block.group("till")),
            "cashier": cashier,
            "shift_no": block.group("shift_no"),
            "start": f"{block.group('start_date')} {block.group('start_time')}",
            "end": f"{block.group('end_date')} {block.group('end_time')}",
            "actual": round(total_actual, 2),
            "theoretical": round(total_theoretical, 2),
            "variance": round(total_variance, 2),
            "cash_actual": round(cash_actual, 2),
            "cash_theoretical": round(cash_theoretical, 2),
            "cash_variance": round(cash_variance, 2),
        })

        totals = cashier_totals.setdefault(cashier, {
            "cashier": cashier,
            "shift_count": 0,
            "actual": 0.0,
            "theoretical": 0.0,
            "variance": 0.0,
            "cash_variance": 0.0,
        })
        totals["shift_count"] += 1
        totals["actual"] += total_actual
        totals["theoretical"] += total_theoretical
        totals["variance"] += total_variance
        totals["cash_variance"] += cash_variance

    if not shifts:
        raise ValueError(f"Cash variance report contained no cashier shift totals: {path}")

    by_cashier = sorted(cashier_totals.values(), key=lambda row: abs(row["variance"]), reverse=True)
    for row in by_cashier:
        row["actual"] = round(row["actual"], 2)
        row["theoretical"] = round(row["theoretical"], 2)
        row["variance"] = round(row["variance"], 2)
        row["cash_variance"] = round(row["cash_variance"], 2)

    largest = by_cashier[0]
    total_actual = round(sum(shift["actual"] for shift in shifts), 2)
    total_theoretical = round(sum(shift["theoretical"] for shift in shifts), 2)
    total_variance = round(sum(shift["variance"] for shift in shifts), 2)
    cash_variance = round(sum(shift["cash_variance"] for shift in shifts), 2)

    return {
        "source_file": path.name,
        "batch": int(batch.group(1)),
        "batch_date": date.group(1),
        "shift_count": len(shifts),
        "cashier_count": len(by_cashier),
        "total_actual": total_actual,
        "total_theoretical": total_theoretical,
        "total_variance": total_variance,
        "cash_variance": cash_variance,
        "largest_variance_cashier": largest["cashier"],
        "largest_variance_amount": largest["variance"],
        "by_cashier": by_cashier,
        "shifts": shifts,
    }


def parse_stock_take_summary(path: Path) -> dict[str, Any]:
    text = read_text(path)
    date = re.search(r"Date:\s*(\d{2}/\d{2}/\d{4})", text)
    variances = re.findall(r"(\-?\d+\.\d+)\s+(\-?\d+\.\d+)\s*$", text, re.M)
    value_at_risk = sum(parse_money(v[1]) for v in variances if parse_money(v[0]) != 0)
    count = sum(1 for v in variances if parse_money(v[0]) != 0)
    return {
        "source_file": path.name,
        "stock_take_date": date.group(1) if date else "",
        "sku_variances": count,
        "variance_value_at_cost": round(value_at_risk, 2),
    }


def pick_latest(files: list[Path]) -> Path | None:
    if not files:
        return None
    primary = [f for f in files if "(1)" not in f.name and "(2)" not in f.name]
    pool = primary if primary else files
    return max(pool, key=lambda p: p.stat().st_mtime)


def pick_latest_day_end(files: list[Path]) -> Path | None:
    """Latest trading day = highest batch number (not filename suffix)."""
    if not files:
        return None
    best = None
    best_batch = -1
    for p in files:
        text = read_text(p)
        m = re.search(r"Batch Number\s*:\s*(\d+)", text)
        batch = int(m.group(1)) if m else 0
        if batch > best_batch:
            best_batch = batch
            best = p
    return best


def discover_pos_dirs(inputs_dir: Path) -> list[Path]:
    """POS exports may live in Starter Docs, Refresh drops, or other sibling folders."""
    if inputs_dir.name in ("Starter Docs", "Refresh"):
        parent = inputs_dir.parent
        dirs: list[Path] = []
        for name in ("Starter Docs", "Refresh", "Additional"):
            p = parent / name
            if p.is_dir():
                dirs.append(p)
        return dirs or [inputs_dir]
    return [inputs_dir]


def glob_pos(pos_dirs: list[Path], pattern: str) -> list[Path]:
    found: list[Path] = []
    for d in pos_dirs:
        found.extend(d.glob(pattern))
    return found


def build_canonical(inputs_dir: Path) -> dict[str, Any]:
    pos_dirs = discover_pos_dirs(inputs_dir)
    day_files = glob_pos(pos_dirs, "Day End Summary*.TXT")
    latest_day = pick_latest_day_end(day_files)
    month_file = pick_latest(glob_pos(pos_dirs, "Month End Summary*.TXT"))
    monthly_cat = pick_latest(glob_pos(pos_dirs, "Monthly Summary Forecourt*.TXT"))
    eft_pending = pick_latest(glob_pos(pos_dirs, "EFT Transactions Not Yet*.TXT"))
    eft_batch = pick_latest(glob_pos(pos_dirs, "EFT Batch Summary*.TXT"))
    stock = pick_latest(glob_pos(pos_dirs, "Stock Take Variance*.TXT"))

    canonical: dict[str, Any] = {
        "generated_from": [str(d) for d in pos_dirs],
        "site": "ENGEN JET PARK SERVICE STATION",
    }

    if latest_day:
        day = parse_day_end(latest_day)
        canonical["daily"] = asdict(day)
        canonical["daily"]["top_categories"] = sorted(
            [asdict(c) for c in day.top_categories],
            key=lambda x: x["total_sales"],
            reverse=True,
        )[:8]
        canonical["daily"]["fuel_grades"] = [asdict(g) for g in day.fuel_grades]
        canonical["daily"]["cashiers"] = [asdict(c) for c in day.cashiers]

    by_batch: dict[int, tuple[int, float, Any]] = {}
    for p in day_files:
        d = parse_day_end(p)
        pri = 0 if "(1)" in p.name else 1
        mtime = p.stat().st_mtime
        key = d.batch_number
        if key not in by_batch or pri > by_batch[key][0] or (pri == by_batch[key][0] and mtime > by_batch[key][1]):
            by_batch[key] = (pri, mtime, d)
    if by_batch:
        canonical["daily_history"] = [
            {
                "batch": d.batch_number,
                "date": d.batch_date,
                "nett_takings": d.nett_takings,
                "fuel_total": d.fuel_total,
                "shop_total": d.shop_total_incl,
                "fuel_volume": d.fuel_volume,
                "cash_variance": d.cash_variance,
            }
            for _, _, d in sorted(by_batch.values(), key=lambda x: x[2].batch_number)
        ]

    if month_file:
        canonical["monthly_april"] = parse_month_end(month_file)
    if monthly_cat:
        canonical["monthly_category_file"] = {"source": monthly_cat.name}
    if eft_pending:
        canonical["eft_pending"] = parse_eft_pending(eft_pending)
    if eft_batch:
        canonical["eft_batch"] = parse_eft_batch_summary(eft_batch)
    if stock:
        canonical["stock_take"] = parse_stock_take_summary(stock)

    # Merge bank / manual recon / inventory from parent inputs folder
    inputs_root = inputs_dir.parent if inputs_dir.name == "Starter Docs" else inputs_dir
    payroll_dir = Path(__file__).resolve().parents[2] / "reports" / "payroll"
    try:
        from parse_external_inputs import build_external_context
        canonical["external"] = build_external_context(inputs_root, canonical, payroll_dir)
    except ImportError:
        pass

    return canonical


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs", nargs="?", default="docs/_ai_context/inputs/Starter Docs")
    parser.add_argument("-o", "--output", default="reports/data/canonical-latest.json")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[2]
    inputs = root / args.inputs
    out = root / args.output
    out.parent.mkdir(parents=True, exist_ok=True)
    data = build_canonical(inputs)
    out.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
