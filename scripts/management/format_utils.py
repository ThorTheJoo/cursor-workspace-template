#!/usr/bin/env python3
"""Standard date and number formatting for management reports (ZA conventions)."""

from __future__ import annotations

import re
from datetime import datetime
from typing import Any


DATE_DISPLAY = "%d/%m/%Y"  # DD/MM/YYYY — matches POS exports


def normalize_date(value: str | None) -> str:
    """Parse mixed inputs → DD/MM/YYYY display string."""
    if not value or not str(value).strip():
        return "—"
    s = str(value).strip()
    if re.match(r"^\d{2}/\d{2}/\d{4}$", s):
        return s
    if re.match(r"^\d{4}-\d{2}-\d{2}$", s):
        dt = datetime.strptime(s, "%Y-%m-%d")
        return dt.strftime(DATE_DISPLAY)
    m = re.match(r"^(\d{1,2})[-/](\w{3})[-/](\d{2,4})$", s, re.I)
    if m:
        day, mon, yr = m.group(1), m.group(2)[:3].title(), m.group(3)
        months = {
            "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
            "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12,
        }
        yyyy = int(yr) if len(yr) == 4 else 2000 + int(yr)
        return datetime(yyyy, months.get(mon, 1), int(day)).strftime(DATE_DISPLAY)
    m2 = re.match(r"^(\d{1,2})\s+(\w+)\s+(\d{4})$", s, re.I)
    if m2:
        return normalize_date(f"{m2.group(1)}-{m2.group(2)[:3]}-{m2.group(4)}")
    return s


def date_sort_key(value: str | None) -> tuple[int, int, int]:
    d = normalize_date(value)
    if d == "—":
        return (9999, 12, 31)
    try:
        dt = datetime.strptime(d, DATE_DISPLAY)
        return (dt.year, dt.month, dt.day)
    except ValueError:
        return (9999, 12, 31)


def iso_date(value: str | None) -> str:
    d = normalize_date(value)
    if d == "—":
        return ""
    dt = datetime.strptime(d, DATE_DISPLAY)
    return dt.strftime("%Y-%m-%d")


def fmt_litres(n: float | None) -> str:
    if n is None:
        return "—"
    return f"{n:,.2f} L"


def fmt_delta(current: float | None, prior: float | None, unit: str = "R") -> str:
    if current is None or prior is None:
        return "—"
    diff = current - prior
    if abs(diff) < 0.005:
        return "±0"
    sign = "+" if diff > 0 else ""
    if unit == "R":
        return f"{sign}R {diff:,.2f}"
    if unit == "L":
        return f"{sign}{diff:,.2f} L"
    return f"{sign}{diff:,.2f}"


def fmt_signed_delta(n: float | None, unit: str = "R") -> str:
    if n is None:
        return "—"
    if abs(n) < 0.005:
        return "±0"
    if unit == "R":
        return f"{'+' if n >= 0 else ''}R {n:,.2f}"
    if unit == "L":
        return f"{'+' if n >= 0 else ''}{n:,.2f} L"
    return f"{'+' if n >= 0 else ''}{n:,.2f}"


def delta_class_from_change(n: float | None, invert: bool = False) -> str:
    if n is None or abs(n) < 0.005:
        return "flat"
    good = n > 0
    if invert:
        good = not good
    return "up" if good else "down"


def build_daily_timeline(
    history: list[dict[str, Any]],
    ocr: dict[str, Any],
) -> list[dict[str, Any]]:
    """Merge POS daily history + OCR fuel/shop/CIT into chronological day rows."""
    by_iso: dict[str, dict[str, Any]] = {}

    for h in history:
        iso = iso_date(h.get("date"))
        if not iso:
            continue
        by_iso[iso] = {
            "date_display": normalize_date(h.get("date")),
            "date_iso": iso,
            "batch": h.get("batch"),
            "nett_takings": h.get("nett_takings"),
            "fuel_total": h.get("fuel_total"),
            "fuel_volume": h.get("fuel_volume"),
            "shop_total": h.get("shop_total"),
            "cash_variance": h.get("cash_variance"),
            "source": "pos_system",
        }

    for fv in ocr.get("fuel_volume_daily", []):
        iso = fv.get("date") if re.match(r"^\d{4}-\d{2}-\d{2}$", str(fv.get("date", ""))) else iso_date(fv.get("date"))
        if not iso:
            continue
        row = by_iso.setdefault(iso, {
            "date_display": normalize_date(iso),
            "date_iso": iso,
            "source": "ocr_whatsapp",
        })
        row["ocr_fuel_litres"] = fv.get("total_litres")

    for sd in ocr.get("shop_daily", []):
        iso = iso_date(sd.get("date")) or sd.get("date", "")
        if not iso or not re.match(r"^\d{4}-\d{2}-\d{2}$", iso):
            iso = sd.get("date", "")
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", str(iso)):
            continue
        row = by_iso.setdefault(iso, {
            "date_display": normalize_date(iso),
            "date_iso": iso,
            "source": "mixed",
        })
        row["ocr_shop_total"] = sd.get("dry_stock_total")

    cit_by_iso: dict[str, float] = {}
    for c in ocr.get("cit_pickups", []):
        if c.get("type") == "cash_drop":
            continue
        iso = c.get("date", "")
        if re.match(r"^\d{4}-\d{2}-\d{2}$", iso):
            cit_by_iso[iso] = cit_by_iso.get(iso, 0) + c.get("amount", 0)

    for iso, amt in cit_by_iso.items():
        row = by_iso.setdefault(iso, {
            "date_display": normalize_date(iso),
            "date_iso": iso,
            "source": "ocr_whatsapp",
        })
        row["cit_pickup"] = amt

    timeline = sorted(by_iso.values(), key=lambda r: r.get("date_iso", ""))

    for i, row in enumerate(timeline):
        if i == 0:
            row["delta_nett"] = None
            row["delta_fuel_l"] = None
            row["delta_shop"] = None
            continue
        prev = timeline[i - 1]
        row["delta_nett"] = (
            (row.get("nett_takings") or 0) - (prev.get("nett_takings") or 0)
            if row.get("nett_takings") is not None and prev.get("nett_takings") is not None
            else None
        )
        row["delta_fuel_l"] = (
            (row.get("fuel_volume") or row.get("ocr_fuel_litres") or 0)
            - (prev.get("fuel_volume") or prev.get("ocr_fuel_litres") or 0)
            if (row.get("fuel_volume") or row.get("ocr_fuel_litres")) is not None
            and (prev.get("fuel_volume") or prev.get("ocr_fuel_litres")) is not None
            else None
        )
        row["delta_shop"] = (
            (row.get("shop_total") or 0) - (prev.get("shop_total") or 0)
            if row.get("shop_total") is not None and prev.get("shop_total") is not None
            else None
        )

    return timeline
