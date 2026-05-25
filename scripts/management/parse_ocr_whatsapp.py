#!/usr/bin/env python3
"""Parse OCR-synthesized WhatsApp report extracts into structured data + reconciliations."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any


RESERVE_L = 1000
MIN_DAYS_STOCK = 5
MAX_PUMP_TANK_VAR_L = 25  # per ~5000 L day


def _parse_date_dmy(text: str) -> str:
    """Convert 21-May-26 or 21 May 2026 → 2026-05-21."""
    m = re.search(r"(\d{1,2})[-/](\w{3})[-/](\d{2,4})", text, re.I)
    if not m:
        m2 = re.search(r"(\d{1,2})\s+(\w{3,9})\s+(\d{4})", text, re.I)
        if not m2:
            return text.strip()
        m = m2
    day, mon, yr = m.group(1), m.group(2)[:3].title(), m.group(3)
    months = {
        "Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06",
        "Jul": "07", "Aug": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12",
    }
    mm = months.get(mon, "01")
    yyyy = yr if len(yr) == 4 else f"20{yr}"
    return f"{yyyy}-{mm}-{int(day):02d}"


def parse_deepseek_ocr(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8", errors="replace")
    result: dict[str, Any] = {
        "source_file": path.name,
        "source_type": "ocr_whatsapp",
        "channel": "WhatsApp JPEG images → OCR synthesis (DeepSeek)",
        "trust": "reference_pending_pos_confirmation",
        "atg_dips": [],
        "fuel_volume_daily": [],
        "pump_tank_eod": [],
        "shop_daily": [],
        "cit_pickups": [],
        "staff_exceptions": [],
        "fuel_margins": {},
        "alerts": [],
        "thresholds": {
            "reserve_litres": RESERVE_L,
            "min_days_stock": MIN_DAYS_STOCK,
            "max_pump_tank_variance_litres": MAX_PUMP_TANK_VAR_L,
        },
    }

    # --- ATG tank dips (section 1 only) ---
    atg_section = re.search(r"1\. FUEL INVENTORY.*?2\. FUEL SALES", text, re.S)
    if atg_section:
        block = atg_section.group(0)
        current_atg: dict[str, Any] | None = None
        for line in block.splitlines():
            img = re.search(r"WhatsApp Image (\d{4}-\d{2}-\d{2})", line)
            if img:
                current_atg = {"date": img.group(1), "products": [], "source_image": line.strip()}
                result["atg_dips"].append(current_atg)
                continue
            if not current_atg:
                continue
            for prod, pattern in [
                ("ULP95", r"ULP95[^:]*:\s*([\d,]+)\s*L"),
                ("Diesel50", r"Diesel50[^:]*:\s*([\d,]+)\s*L"),
                ("ULP93", r"ULP93[^:]*:\s*([\d,]+)\s*L"),
            ]:
                m = re.search(pattern, line, re.I)
                if m and not any(p["product"] == prod for p in current_atg["products"]):
                    litres = float(m.group(1).replace(",", ""))
                    current_atg["products"].append({
                        "product": prod,
                        "litres": litres,
                        "reserve": RESERVE_L,
                        "available": litres - RESERVE_L,
                    })

    # Days-of-stock KPI lines
    for line in text.splitlines():
        m = re.search(
            r"(ULP95|Diesel50|ULP93)\s+avg\s+([\d.]+)\s*L/day.*?24 May:\s*([\d.]+)\s*days",
            line,
            re.I,
        )
        if m:
            prod, avg, days = m.group(1), float(m.group(2)), float(m.group(3))
            entry = next((a for a in result.get("_days_stock", []) if a["product"] == prod), None)
            if not result.get("_days_stock"):
                result["_days_stock"] = []
            result["_days_stock"].append({
                "product": prod.upper() if prod.upper().startswith("ULP") else prod,
                "avg_daily_litres": avg,
                "days_stock_24may": days,
                "below_threshold": days < MIN_DAYS_STOCK,
            })

    if "_days_stock" in result:
        result["days_of_stock"] = result.pop("_days_stock")

    # --- Daily fuel volume ---
    fuel_section = re.search(r"2\. FUEL SALES.*?3\. SHOP", text, re.S)
    if fuel_section:
        for line in fuel_section.group(0).splitlines():
            m = re.search(
                r"(\d{1,2}-May-26):\s*ULP95\s+([\d,]+\.?\d*)\s*L,\s*ULP93\s+([\d,]+\.?\d*)\s*L,\s*Diesel\s+([\d,]+\.?\d*)\s*L.*?Total\s+([\d,]+\.?\d*)\s*L",
                line,
            )
            if m:
                result["fuel_volume_daily"].append({
                    "date": _parse_date_dmy(m.group(1)),
                    "ulp95": float(m.group(2).replace(",", "")),
                    "ulp93": float(m.group(3).replace(",", "")),
                    "diesel": float(m.group(4).replace(",", "")),
                    "total_litres": float(m.group(5).replace(",", "")),
                })

    # --- Pump vs tank EOD (file line + next line) ---
    if fuel_section:
        lines = fuel_section.group(0).splitlines()
        for i, line in enumerate(lines):
            batch_m = re.search(r"Batch\s+(\d+)\s+EOD.*?(\d{1,2}\s+\w+\s+\d{4})", line, re.I)
            if batch_m and i + 1 < len(lines):
                pump_line = lines[i + 1]
                pm = re.search(
                    r"Pump sales:\s*([\d,]+\.?\d*)\s*L.*?Tank sales:\s*([\d,]+)\s*L.*?Variance:\s*([+-]?[\d.]+)\s*L",
                    pump_line,
                )
                if pm:
                    var = float(pm.group(3))
                    result["pump_tank_eod"].append({
                        "batch": int(batch_m.group(1)),
                        "date": _parse_date_dmy(batch_m.group(2)),
                        "pump_litres": float(pm.group(1).replace(",", "")),
                        "tank_litres": float(pm.group(2).replace(",", "")),
                        "variance_litres": var,
                        "status": "ok" if abs(var) <= MAX_PUMP_TANK_VAR_L else "review",
                        "note": pump_line.split("–")[-1].strip() if "–" in pump_line else "",
                    })

    # --- Shop daily ---
    shop_section = re.search(r"3\. SHOP.*?4\. CASH", text, re.S)
    if shop_section:
        for line in shop_section.group(0).splitlines():
            m = re.search(
                r"(\d{1,2}-May):\s*Shop Total\s*R([\d,]+\.?\d*),\s*Dry Stock(?: Total)?\s*R([\d,]+\.?\d*),\s*Bakery\s*R([\d,]+\.?\d*)",
                line,
            )
            if m:
                result["shop_daily"].append({
                    "date": _parse_date_dmy(f"{m.group(1)}-26"),
                    "shop_total": float(m.group(2).replace(",", "")),
                    "dry_stock_total": float(m.group(3).replace(",", "")),
                    "bakery": float(m.group(4).replace(",", "")),
                })

    # --- CIT pickups ---
    cit_section = re.search(r"4\. CASH MANAGEMENT(.*?)5\. SHIFT", text, re.S)
    if cit_section:
        result["cit_pickups"] = []
        for line in cit_section.group(1).splitlines():
            m = re.search(r"Image (\d{4}-\d{2}-\d{2}).*?Total\s*R([\d,]+)", line)
            if m:
                result["cit_pickups"].append({
                    "date": m.group(1),
                    "amount": float(m.group(2).replace(",", "")),
                })
            drop = re.search(r"Drop\s*R([\d,]+)", line)
            if drop and "CAROLINE" in line:
                result["cit_pickups"].append({
                    "date": "2026-05-15",
                    "amount": float(drop.group(1).replace(",", "")),
                    "type": "cash_drop",
                    "operator": "CAROLINE",
                })

    # --- Staff exceptions ---
    if "SIA" in text and "+R1,110.25" in text:
        result["staff_exceptions"].append({
            "operator": "SIA",
            "date": "2026-05-18",
            "variance": 1110.25,
            "direction": "over",
            "status": "investigate",
        })

    # --- Alerts ---
    if "DELIVERY NEEDED" in text:
        result["alerts"].append({
            "type": "delivery_needed",
            "product": "ULP95",
            "date": "2026-05-16",
            "message": "ATG alarm — ULP95 tank below reorder level",
        })
    for ds in result.get("days_of_stock", []):
        if ds.get("below_threshold"):
            result["alerts"].append({
                "type": "low_days_stock",
                "product": ds["product"],
                "days": ds["days_stock_24may"],
                "message": f"{ds['product']} at {ds['days_stock_24may']:.1f} days — below {MIN_DAYS_STOCK}-day safety target",
            })

    # --- Fuel margins snapshot ---
    margin_block = re.search(
        r"Fuel Rand Value 21 May(.*?)File: WhatsApp Image 2026-05-22 at 08.18",
        text,
        re.S,
    )
    if margin_block:
        for prod, pat in [
            ("ULP95", r"ULP95: Sell R([\d.]+)/L, Cost R([\d.]+).*?([\d.]+)%"),
            ("ULP93", r"ULP93: Sell R([\d.]+)/L, Cost R([\d.]+).*?([\d.]+)%"),
            ("Diesel50", r"Diesel50: Sell R([\d.]+)/L, Cost R([\d.]+).*?([\d.]+)%"),
        ]:
            m = re.search(pat, margin_block.group(1))
            if m:
                result["fuel_margins"][prod] = {
                    "sell_per_l": float(m.group(1)),
                    "cost_per_l": float(m.group(2)),
                    "margin_pct": float(m.group(3)),
                }

    return result


def build_reconciliations(ocr: dict[str, Any], canonical: dict[str, Any]) -> list[dict[str, Any]]:
    """Cross-source comparison rows: source A vs source B with variance and status."""
    rows: list[dict[str, Any]] = []
    daily = canonical.get("daily", {})
    history = {h.get("date", ""): h for h in canonical.get("daily_history", [])}

    # Map POS by ISO date
    pos_by_date: dict[str, dict] = {}
    for h in canonical.get("daily_history", []):
        d = h.get("date", "")
        parts = d.split("/")
        if len(parts) == 3:
            iso = f"{parts[2]}-{parts[1]}-{parts[0]}"
            pos_by_date[iso] = h

    # Also parse batch 143 from available day-end files if not in history
    for h in canonical.get("daily_history", []):
        if h.get("batch") == 143:
            parts = h.get("date", "").split("/")
            if len(parts) == 3:
                pos_by_date[f"{parts[2]}-{parts[1]}-{parts[0]}"] = h

    # 1. OCR daily fuel volume vs POS (where dates match)
    for fv in ocr.get("fuel_volume_daily", []):
        iso = fv["date"]
        pos = pos_by_date.get(iso)
        if pos and pos.get("fuel_volume"):
            pos_vol = pos["fuel_volume"]
            diff = round(fv["total_litres"] - pos_vol, 2)
            rows.append({
                "check": "Daily fuel volume (L)",
                "date": iso,
                "source_a": "ocr_whatsapp",
                "value_a": fv["total_litres"],
                "label_a": "OCR WhatsApp report",
                "source_b": "pos_system",
                "value_b": pos_vol,
                "label_b": f"POS Batch {pos.get('batch', '?')}",
                "variance": diff,
                "unit": "L",
                "status": "match" if abs(diff) < 1 else "review",
            })

    # 2. OCR shop dry stock vs POS shop incl (Batch 143 / 20 May known match)
    for sd in ocr.get("shop_daily", []):
        iso = sd["date"]
        pos = pos_by_date.get(iso)
        if pos and pos.get("shop_total"):
            diff = round(sd["dry_stock_total"] - pos["shop_total"], 2)
            rows.append({
                "check": "Shop sales (incl VAT)",
                "date": iso,
                "source_a": "ocr_whatsapp",
                "value_a": sd["dry_stock_total"],
                "label_a": "OCR Dry Stock Total",
                "source_b": "pos_system",
                "value_b": pos["shop_total"],
                "label_b": f"POS Shop Incl (Batch {pos.get('batch', '?')})",
                "variance": diff,
                "unit": "R",
                "status": "match" if abs(diff) < 1 else "review",
            })

    # 3. OCR pump-tank EOD (internal wet stock control from images)
    for pt in ocr.get("pump_tank_eod", []):
        rows.append({
            "check": "Pump vs tank variance (EOD)",
            "date": pt["date"],
            "source_a": "ocr_whatsapp",
            "value_a": pt["pump_litres"],
            "label_a": f"OCR pump meters (Batch {pt['batch']})",
            "source_b": "ocr_whatsapp",
            "value_b": pt["tank_litres"],
            "label_b": f"OCR ATG dip (Batch {pt['batch']})",
            "variance": pt["variance_litres"],
            "unit": "L",
            "status": pt["status"],
            "note": pt.get("note", ""),
        })

    # 4. POS wet stock (latest day end) vs threshold
    for g in daily.get("fuel_grades", []):
        v = g.get("variance_litres", 0)
        rows.append({
            "check": f"Wet stock — {g.get('description', g.get('grade_id', ''))}",
            "date": daily.get("batch_date", ""),
            "source_a": "pos_system",
            "value_a": g.get("pump_volume", 0),
            "label_a": "POS pump volume",
            "source_b": "pos_system",
            "value_b": g.get("tank_volume", 0),
            "label_b": "POS tank dip",
            "variance": v,
            "unit": "L",
            "status": "ok" if abs(v) <= MAX_PUMP_TANK_VAR_L else "review",
            "note": "Target ±25 L per grade per day",
        })

    # 5–6. Bank reconciliations (payroll + EFT vs Speedpoint) handled in parse_external_inputs
    cit_by_date = {c["date"]: c for c in ocr.get("cit_pickups", []) if c.get("type") != "cash_drop"}
    for fv in ocr.get("fuel_volume_daily", []):
        iso = fv["date"]
        cit = cit_by_date.get(iso)
        shop = next((s for s in ocr.get("shop_daily", []) if s["date"] == iso), None)
        if cit and shop:
            est_sales = shop["dry_stock_total"]  # proxy; full fuel rand not in daily OCR table
            rows.append({
                "check": "CIT pickup vs shop turnover",
                "date": iso,
                "source_a": "ocr_whatsapp",
                "value_a": cit["amount"],
                "label_a": "CIT bag removal (camera/OCR)",
                "source_b": "ocr_whatsapp",
                "value_b": shop["dry_stock_total"],
                "label_b": "OCR shop sales (excl fuel rand)",
                "variance": round(cit["amount"] - shop["dry_stock_total"], 2),
                "unit": "R",
                "status": "info",
                "note": "CIT is cash-only; shop figure excludes fuel and cards — low CIT vs total sales is normal",
            })

    return rows


def find_ocr_files(inputs_root: Path) -> list[Path]:
    patterns = ["deepseek*.txt", "*ocr*.txt", "*whatsapp*.txt"]
    found: list[Path] = []
    for pat in patterns:
        found.extend(inputs_root.glob(pat))
    return sorted(set(found), key=lambda p: p.stat().st_mtime, reverse=True)


def build_ocr_context(inputs_root: Path, canonical: dict[str, Any] | None = None) -> dict[str, Any]:
    files = find_ocr_files(inputs_root)
    if not files:
        return {}
    parsed = parse_deepseek_ocr(files[0])
    ctx: dict[str, Any] = {"ocr_whatsapp": parsed}
    if canonical:
        ctx["reconciliations"] = build_reconciliations(parsed, canonical)
    return ctx
