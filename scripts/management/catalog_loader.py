#!/usr/bin/env python3
"""Load file-type-catalog.yaml for drill-down and help pages."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
CATALOG_PATH = ROOT / "docs" / "_ai_context" / "knowledge" / "reference" / "file-type-catalog.yaml"


def load_catalog() -> dict[str, Any]:
    if not CATALOG_PATH.exists():
        return {}
    data = yaml.safe_load(CATALOG_PATH.read_text(encoding="utf-8"))
    return data.get("report_types", {}) or {}


def get_report_spec(report_type: str) -> dict[str, Any]:
    return load_catalog().get(report_type, {})


def frequency_label(freq: str) -> str:
    return {
        "daily": "Daily",
        "weekly": "Weekly",
        "weekly_to_monthly": "Weekly / Monthly",
        "monthly": "Monthly",
        "month_end": "Month-end",
        "periodic": "Periodic",
        "ad_hoc": "Ad hoc",
        "per_pay_run": "Per pay run",
        "ongoing": "Ongoing",
        "static": "Static template",
    }.get(freq, freq.replace("_", " ").title())
