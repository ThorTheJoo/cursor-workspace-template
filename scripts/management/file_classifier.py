#!/usr/bin/env python3
"""Classify input files to report_type_id for file repo / MDD catalog."""

from __future__ import annotations

import re
from pathlib import Path

# Order matters: first match wins
REPORT_PATTERNS: list[tuple[str, str, str]] = [
    (r"day end summary", "day_end_summary", "pos_system"),
    (r"month end summary", "month_end_summary", "pos_system"),
    (r"month end detail", "month_end_detail", "pos_system"),
    (r"eom by category", "eom_category_detail", "pos_system"),
    (r"monthly summary forecourt", "monthly_category_summary", "pos_system"),
    (r"cash variance", "cash_variance_by_cashier", "pos_system"),
    (r"eft batch summary", "eft_batch_summary", "pos_system"),
    (r"eft summary by eod", "eft_summary_by_shift", "pos_system"),
    (r"eft detail", "eft_detail_by_shift", "pos_system"),
    (r"eft transactions not yet", "eft_pending", "pos_system"),
    (r"stock take variance", "stock_take_variance", "inventory"),
    (r"stock shrinkage", "stock_shrinkage_mtd", "inventory"),
    (r"stock purchases summary.*summarized", "stock_purchases_summarized", "inventory"),
    (r"stock purchases summary", "stock_purchases_by_category", "inventory"),
    (r"stock on hand", "stock_on_hand", "inventory"),
    (r"stock cost.*selling price", "stock_cost_sell_price", "inventory"),
    (r"fuel sales control.*mtd by product", "fuel_control_mtd_by_product", "pos_system"),
    (r"fuel sales control.*atg", "fuel_control_atg", "pos_system"),
    (r"fuel sales control.*mtd summary", "fuel_control_mtd_summary", "pos_system"),
    (r"turnover levy", "turnover_levy", "accounting"),
    (r"debtors age", "debtors_age_analysis", "accounting"),
    (r"creditors purchases", "creditors_purchases_detail", "accounting"),
    (r"nett pay list", "nett_pay_list", "payroll_system"),
    (r"deepseek|ocr|whatsapp", "ocr_synthesis", "ocr_whatsapp"),
    (r"cash up", "cash_up", "manual_recon"),
    (r"schedule of accounts", "supplier_schedule", "manual_recon"),
    (r"\.ofx$", "bank_statement", "bank_feed"),
    (r"payment_.*\.csv$", "payment_csv", "payroll_system"),
]


def normalize_pattern_name(filename: str) -> str:
    """Strip duplicate suffixes like (1), (2) for grouping."""
    base = Path(filename).stem
    return re.sub(r"\s*\(\d+\)\s*$", "", base).strip()


def classify_report(path: Path) -> dict[str, str]:
    name = path.name.lower()
    stem = normalize_pattern_name(path.name).lower()
    for pattern, report_type, source_type in REPORT_PATTERNS:
        if re.search(pattern, stem) or re.search(pattern, name):
            return {
                "report_type": report_type,
                "source_type": source_type,
                "pattern_name": normalize_pattern_name(path.name),
            }
    ext = path.suffix.lower()
    if ext == ".txt":
        return {"report_type": "pos_unknown_txt", "source_type": "pos_system", "pattern_name": stem}
    if ext in (".xls", ".xlsx"):
        return {"report_type": "spreadsheet_unknown", "source_type": "manual_recon", "pattern_name": stem}
    return {"report_type": "unknown", "source_type": "unknown", "pattern_name": stem}


def is_duplicate_copy(filename: str) -> bool:
    """Windows-style duplicate of same export — (1) only. (2)(3) in Additional are distinct batches."""
    return bool(re.search(r"\s*\(1\)\s*\.(TXT|txt|xls|xlsx|ofx|csv)$", filename, re.I))
