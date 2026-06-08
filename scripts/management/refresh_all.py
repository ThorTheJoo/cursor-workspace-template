#!/usr/bin/env python3
"""Agent-friendly refresh entry point for the Experiment JP reporting stack."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "payroll"))

from validate_payment_csv import validate_payment_csv


def run_step(name: str, command: list[str]) -> dict[str, Any]:
    started = datetime.now(timezone.utc).isoformat(timespec="seconds")
    result = subprocess.run(command, cwd=str(ROOT), text=True, capture_output=True)
    return {
        "name": name,
        "command": command,
        "started_at": started,
        "returncode": result.returncode,
        "ok": result.returncode == 0,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
    }


def validate_payment_outputs(own_account: str | None = None) -> list[dict[str, Any]]:
    payroll_dir = ROOT / "reports" / "payroll"
    if not payroll_dir.exists():
        return []
    return [
        validate_payment_csv(path, own_account)
        for path in sorted(payroll_dir.glob("Payment_*.csv"))
        if " (1)" not in path.name
    ]


def build_status(steps: list[dict[str, Any]], payment_validations: list[dict[str, Any]]) -> dict[str, Any]:
    outputs = {
        "dashboard": "reports/management-dashboard.html",
        "canonical": "reports/data/canonical-latest.json",
        "ledger": "reports/data/ingest-ledger.json",
        "file_repo_index": "reports/file-views/index.html",
        "payroll_dir": "reports/payroll",
    }
    missing_outputs = [
        rel_path
        for rel_path in outputs.values()
        if not (ROOT / rel_path).exists()
    ]
    validation_errors = [
        error
        for validation in payment_validations
        for error in validation.get("errors", [])
    ]
    ok = all(step["ok"] for step in steps) and not missing_outputs and not validation_errors
    return {
        "ok": ok,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "workspace": str(ROOT),
        "steps": steps,
        "payment_csv_validations": payment_validations,
        "outputs": outputs,
        "missing_outputs": missing_outputs,
        "agent_next_action": "review_dashboard" if ok else "human_review_required",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Refresh all Experiment JP reports for agent OS workflows")
    parser.add_argument("--json-out", default="reports/data/agent-refresh-status.json")
    parser.add_argument("--own-account", default=None, help="Expected FNB nominated account for payment CSV validation")
    parser.add_argument("--skip-dashboard", action="store_true", help="Only validate existing outputs")
    args = parser.parse_args()

    steps: list[dict[str, Any]] = []
    if not args.skip_dashboard:
        steps.append(run_step(
            "generate_dashboard",
            [sys.executable, "scripts/management/generate_dashboard.py"],
        ))

    validations = validate_payment_outputs(args.own_account)
    status = build_status(steps, validations)
    out_path = ROOT / args.json_out
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(status, indent=2), encoding="utf-8")
    print(json.dumps(status, indent=2))
    if not status["ok"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
