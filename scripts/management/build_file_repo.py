#!/usr/bin/env python3
"""
Build file ingestion ledger, time-series snapshots, and drill-down index.

Architecture: one ledger row per physical file drop; series keyed by business id
(batch/date/period), not filename. See FILE_INGESTION_ARCHITECTURE.md.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "management"))

from file_classifier import classify_report, is_duplicate_copy, normalize_pattern_name
from parse_external_inputs import find_ofx_file, parse_ofx, should_skip_inventory_file

DATA_DIR = ROOT / "reports" / "data"
INPUTS_ROOT = ROOT / "docs" / "_ai_context" / "inputs"
CATALOG_PATH = ROOT / "docs" / "_ai_context" / "knowledge" / "reference" / "file-type-catalog.yaml"


def infer_ingest_channel(rel_path: str) -> str:
    """Infer the agent intake channel from the path under docs/_ai_context/inputs."""
    parts = [part.lower() for part in rel_path.split("/")]
    if "email" in parts:
        return "email"
    if "onedrive" in parts:
        return "onedrive"
    if "manual" in parts:
        return "manual_upload"
    if "inbox" in parts:
        return "agent_inbox"
    return "local_drop"


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()[:16]


def extract_content_key(path: Path, meta: dict[str, str], text: str | None) -> str:
    rt = meta["report_type"]
    if rt == "day_end_summary" and text:
        b = re.search(r"Batch Number\s*:\s*(\d+)", text)
        d = re.search(r"Batch Date\s*:\s*(\d{2}/\d{2}/\d{4})", text)
        if b and d:
            return f"day_end|batch:{b.group(1)}|date:{d.group(1)}"
    if rt == "eft_batch_summary" and text:
        d = re.search(r"From EFT Batch Date\s+(\d{2}/\d{2}/\d{4})", text)
        if d:
            return f"eft_batch|date:{d.group(1)}"
    if rt == "cash_variance_by_cashier" and text:
        b = re.search(r"Batch No\s*:\s*(\d+)", text)
        d = re.search(r"Batch Date\s*:\s*(\d{2}/\d{2}/\d{4})", text)
        if b and d:
            return f"cash_variance|batch:{b.group(1)}|date:{d.group(1)}"
    if rt == "bank_statement":
        return f"bank|account:62848015857|file:{path.name}"
    if rt == "nett_pay_list":
        m = re.search(r"(\d{6})", path.stem)
        return f"payroll|period:{m.group(1)}" if m else f"payroll|file:{path.name}"
    if rt == "stock_take_variance" and text:
        d = re.search(r"Date:\s*(\d{2}/\d{2}/\d{4})", text)
        if d:
            return f"stock_take|date:{d.group(1)}"
    return f"{rt}|file:{normalize_pattern_name(path.name)}"


def extract_summary(path: Path, meta: dict[str, str], text: str | None) -> dict[str, Any]:
    summary: dict[str, Any] = {"report_type": meta["report_type"]}
    if not text:
        return summary
    rt = meta["report_type"]
    if rt == "day_end_summary":
        try:
            from parse_reports import parse_day_end

            d = parse_day_end(path)
            summary.update({
                "batch": d.batch_number,
                "batch_date": d.batch_date,
                "nett_takings": d.nett_takings,
                "fuel_total": d.fuel_total,
                "shop_total_incl": d.shop_total_incl,
                "fuel_volume": d.fuel_volume,
                "cash_variance": d.cash_variance,
            })
        except Exception as e:
            summary["parse_error"] = str(e)
    elif rt == "eft_batch_summary":
        from parse_reports import parse_eft_batch_summary

        summary.update(parse_eft_batch_summary(path))
    elif rt == "cash_variance_by_cashier":
        from parse_reports import parse_cash_variance_by_cashier

        summary.update(parse_cash_variance_by_cashier(path))
    elif rt == "eft_pending":
        from parse_reports import parse_eft_pending

        summary.update(parse_eft_pending(path))
    elif rt == "stock_take_variance":
        from parse_reports import parse_stock_take_summary

        summary.update(parse_stock_take_summary(path))
    return summary


def scan_all_inputs() -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    if not INPUTS_ROOT.exists():
        return entries
    for path in sorted(INPUTS_ROOT.rglob("*")):
        if not path.is_file() or path.name.startswith("."):
            continue
        if should_skip_inventory_file(path):
            continue
        rel = str(path.relative_to(INPUTS_ROOT)).replace("\\", "/")
        meta = classify_report(path)
        text = None
        if path.suffix.upper() == ".TXT":
            text = path.read_text(encoding="utf-8", errors="replace")
        elif path.suffix.lower() == ".ofx":
            text = path.read_text(encoding="utf-8", errors="replace")
        content_key = extract_content_key(path, meta, text)
        summary = extract_summary(path, meta, text)
        entries.append({
            "ingest_id": f"{datetime.now(timezone.utc).strftime('%Y%m%d')}-{file_sha256(path)}",
            "path": rel,
            "filename": path.name,
            "folder": rel.split("/")[0] if "/" in rel else ".",
            "ingest_channel": infer_ingest_channel(rel),
            "pattern_name": meta["pattern_name"],
            "report_type": meta["report_type"],
            "source_type": meta["source_type"],
            "content_key": content_key,
            "is_duplicate_copy": is_duplicate_copy(path.name),
            "size_bytes": path.stat().st_size,
            "modified": datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d %H:%M"),
            "sha256_prefix": file_sha256(path),
            "summary": summary,
            "catalog_ref": f"file-type-catalog.yaml#{meta['report_type']}",
        })
    return entries


def _ledger_pick_score(row: dict[str, Any]) -> tuple:
    """Lower is better: prefer non-(1) copies, then latest modified."""
    dup = 1 if row.get("is_duplicate_copy") else 0
    return (dup, row.get("modified", ""))


def build_series(ledger: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    """Series per report_type, one point per content_key (best physical file wins)."""
    by_type: dict[str, dict[str, dict[str, Any]]] = {}
    best_score: dict[str, dict[str, tuple]] = {}

    for row in ledger:
        rt = row["report_type"]
        ck = row["content_key"]
        score = _ledger_pick_score(row)
        candidate = {
            "content_key": ck,
            "source_file": row["filename"],
            "path": row["path"],
            "modified": row["modified"],
            "summary": row["summary"],
            "ingest_id": row.get("ingest_id", ""),
        }
        by_type.setdefault(rt, {})
        best_score.setdefault(rt, {})
        if ck not in by_type[rt] or score < best_score[rt][ck]:
            by_type[rt][ck] = candidate
            best_score[rt][ck] = score

    def sort_key(point: dict[str, Any]) -> str:
        s = point.get("summary", {})
        return (
            s.get("batch_date")
            or s.get("period_end")
            or s.get("period_start")
            or s.get("pay_date")
            or point.get("modified", "")
        )

    return {
        rt: sorted(items.values(), key=sort_key)
        for rt, items in by_type.items()
    }


def build_type_index(ledger: list[dict[str, Any]], series: dict[str, list]) -> dict[str, Any]:
    types: dict[str, Any] = {}
    for row in ledger:
        rt = row["report_type"]
        if rt not in types:
            types[rt] = {
                "report_type": rt,
                "source_type": row["source_type"],
                "pattern_name": row["pattern_name"],
                "catalog_ref": row["catalog_ref"],
                "file_count": 0,
                "primary_count": 0,
                "series_points": len(series.get(rt, [])),
                "folders": set(),
            }
        types[rt]["file_count"] += 1
        if not row["is_duplicate_copy"]:
            types[rt]["primary_count"] += 1
        types[rt]["folders"].add(row["folder"])
    for t in types.values():
        t["folders"] = sorted(t["folders"])
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "inputs_root": str(INPUTS_ROOT),
        "catalog_path": "docs/_ai_context/knowledge/reference/file-type-catalog.yaml",
        "architecture_doc": "docs/_ai_context/knowledge/FILE_INGESTION_ARCHITECTURE.md",
        "dashboard_spec": "docs/_ai_context/knowledge/MANAGEMENT_DASHBOARD_SPECIFICATION.md",
        "interpretation_guide": "docs/_ai_context/guides/DATA_INTERPRETATION_GUIDE.md",
        "report_types": sorted(types.values(), key=lambda x: x["report_type"]),
        "total_files": len(ledger),
        "total_primary": sum(1 for r in ledger if not r["is_duplicate_copy"]),
    }


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    ledger = scan_all_inputs()
    series = build_series(ledger)
    index = build_type_index(ledger, series)

    (DATA_DIR / "ingest-ledger.json").write_text(
        json.dumps({"entries": ledger, "count": len(ledger)}, indent=2),
        encoding="utf-8",
    )
    series_dir = DATA_DIR / "series"
    series_dir.mkdir(exist_ok=True)
    for rt, points in series.items():
        safe = rt.replace("/", "_")
        (series_dir / f"{safe}.json").write_text(
            json.dumps({"report_type": rt, "points": points}, indent=2),
            encoding="utf-8",
        )
    (DATA_DIR / "file-repo-index.json").write_text(json.dumps(index, indent=2), encoding="utf-8")
    print(f"Ledger: {len(ledger)} files -> {DATA_DIR / 'ingest-ledger.json'}")
    print(f"Series: {len(series)} report types -> {series_dir}/")
    print(f"Index: {index['total_primary']} primary -> {DATA_DIR / 'file-repo-index.json'}")


if __name__ == "__main__":
    main()
