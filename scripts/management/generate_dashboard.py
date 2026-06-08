#!/usr/bin/env python3
"""Generate lightweight management dashboard HTML from canonical JSON + payroll."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "management"))
from format_utils import (
    build_daily_timeline,
    date_sort_key,
    delta_class_from_change,
    fmt_delta,
    fmt_litres,
    fmt_signed_delta,
    normalize_date,
)
from kpi_tooltips import src_badge, tip_html  # noqa: E402


def kpi_context(as_of: str, batch: int | str | None = None, note: str = "") -> str:
    parts = [f"As of <strong>{normalize_date(as_of)}</strong>"]
    if batch:
        parts.append(f"Batch <strong>B{batch}</strong>")
    if note:
        parts.append(note)
    return f'<p class="card-context">{" · ".join(parts)}</p>'


def fmt_zar(n: float) -> str:
    return f"R {n:,.2f}"


def h2(title: str, tip_key: str, source: str | None = None) -> str:
    badge = f" {src_badge(source)}" if source else ""
    return f"<h2>{title}{badge}{tip_html(tip_key)}</h2>"


def load_file_repo_index() -> dict:
    path = ROOT / "reports" / "data" / "file-repo-index.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def run_parsers(inputs_dir: Path, json_path: Path) -> dict:
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "management" / "parse_reports.py"),
            str(inputs_dir),
            "-o",
            str(json_path),
        ],
        check=True,
        cwd=str(ROOT / "scripts" / "management"),
    )
    return json.loads(json_path.read_text(encoding="utf-8"))


def run_all_payroll() -> list[dict]:
    sys.path.insert(0, str(ROOT / "scripts" / "payroll"))
    from netpay_to_payment_csv import convert, find_payroll_files  # noqa: WPS433

    files = find_payroll_files(ROOT / "docs" / "_ai_context" / "inputs")
    results = []
    for pay_file in files:
        stem = pay_file.stem.replace("Nett Pay List - ", "").strip(" -")
        out_csv = ROOT / "reports" / "payroll" / f"Payment_{stem}.csv"
        results.append(convert(pay_file, out_csv, ROOT / "config" / "site.yaml"))
    return sorted(results, key=lambda r: r["pay_date"], reverse=True)


def build_html(data: dict, payroll_runs: list[dict], file_repo: dict | None = None) -> str:
    daily = data.get("daily", {})
    monthly = data.get("monthly_april", {})
    eft = data.get("eft_batch", {})
    pending = data.get("eft_pending", {})
    stock = data.get("stock_take", {})
    history = data.get("daily_history", [])
    external = data.get("external", {})
    bank = external.get("bank_statement", {})
    supplier = external.get("supplier_schedule", {})
    cash_up = external.get("cash_up", {})
    inventory = external.get("input_inventory", [])
    ocr = external.get("ocr_whatsapp", {})
    reconciliations = external.get("reconciliations", [])

    fuel_grades = daily.get("fuel_grades", [])
    categories = daily.get("top_categories", [])
    cashiers = daily.get("cashiers", [])
    mtd_var = daily.get("mtd_fuel_variance_pct", {})
    fuel_var_total = sum(g.get("variance_litres", 0) for g in fuel_grades)

    cat_rows = "".join(
        f"<tr><td>{c['category']}</td><td class='num'>{fmt_zar(c['total_sales'])}</td>"
        f"<td class='num'>{c['gp_percent']:.1f}%</td></tr>"
        for c in categories[:6]
    )
    grade_rows = "".join(
        f"<tr><td>{g['description']}</td><td class='num'>{g['pump_volume']:,.1f} L</td>"
        f"<td class='num'>{fmt_zar(g['amount'])}</td>"
        f"<td class='num {'warn' if abs(g['variance_litres']) > 5 else ''}'>{g['variance_litres']:+.2f} L</td></tr>"
        for g in fuel_grades
    )
    cashier_rows = "".join(
        f"<tr><td>{c['cashier']}</td><td class='num'>{fmt_zar(c['nett_takings'])}</td>"
        f"<td class='num'>{c['void_qty']}</td><td class='num'>{fmt_zar(c['void_amount'])}</td></tr>"
        for c in cashiers
    )
    hist_rows = "".join(
        f"<tr><td class='nowrap'>{normalize_date(h['date'])}</td><td>B{h['batch']}</td>"
        f"<td class='num'>{fmt_zar(h['nett_takings'])}</td>"
        f"<td class='num'>{fmt_litres(h.get('fuel_volume'))}</td>"
        f"<td class='num'>{fmt_zar(h.get('shop_total', 0))}</td>"
        f"<td class='num {'warn' if abs(h['cash_variance']) > 50 else ''}'>{fmt_zar(h['cash_variance'])}</td></tr>"
        for h in sorted(history, key=lambda x: date_sort_key(x.get("date")))
    )
    mtd_var_rows = "".join(
        f"<tr><td>{k}</td><td class='num'>{v:.2f}%</td></tr>" for k, v in mtd_var.items()
    )

    inv_items = [i for i in inventory if i.get("source_type") != "unknown"][:15]
    inv_rows = "".join(
        f"<tr><td><span class='tag tag-{i.get('source_type','unknown')}'>{i.get('source_type','?')}</span></td>"
        f"<td>{i['name']}</td><td>{i.get('report','')}</td><td>{i.get('modified','')}</td></tr>"
        for i in inv_items
    )

    file_repo = file_repo or {}
    repo_types = file_repo.get("report_types", [])
    repo_type_ids = {t.get("report_type") for t in repo_types}
    repo_rows = "".join(
        f"<tr><td><a href='file-views/{t['report_type']}.html'><code>{t['report_type']}</code></a></td>"
        f"<td>{src_badge(t.get('source_type', ''))}</td>"
        f"<td>{t.get('pattern_name', '')}</td>"
        f"<td class='num'>{t.get('primary_count', 0)}</td>"
        f"<td class='num'>{t.get('series_points', 0)}</td>"
        f"<td>{', '.join(t.get('folders', []))}</td></tr>"
        for t in repo_types
    )
    file_repo_section = ""
    if repo_types:
        file_repo_section = f"""
  <section class="card" id="file-repository">
    {h2('File Repository — report types & history', 'file_repository')}
    <p class="note">
      Specs: <code>docs/_ai_context/knowledge/reference/file-type-catalog.yaml</code> ·
      Guide: <code>docs/_ai_context/guides/DATA_INTERPRETATION_GUIDE.md</code> ·
      Ledger: <code>reports/data/ingest-ledger.json</code> ·
      Series: <code>reports/data/series/</code>
    </p>
    <p class="note">Scanned <strong>{file_repo.get('total_primary', 0)}</strong> primary files
      ({file_repo.get('total_files', 0)} total including duplicate copies).
      Click a report type to open history, trends, per-file detail, and help.</p>
    <p class="toolbar" style="margin:.5rem 0">
      <a class="btn" href="file-views/index.html" style="display:inline-block;padding:.35rem .75rem;background:#e65100;color:#fff;border-radius:6px;text-decoration:none;font-weight:600">Open full File Repository</a>
    </p>
    <table><thead><tr>
      <th>Report type</th><th>Source</th><th>Pattern</th>
      <th class="num">Files</th><th class="num">Series pts</th><th>Folders</th>
    </tr></thead>
    <tbody>{repo_rows}</tbody></table>
  </section>"""

    def fmt_val(v: float | None, unit: str) -> str:
        if v is None:
            return "—"
        if unit == "R":
            return fmt_zar(v)
        if unit == "L":
            return fmt_litres(v)
        return str(v)

    def status_class(s: str) -> str:
        return {"match": "ok", "ok": "ok", "review": "warn", "pending": "", "info": ""}.get(s, "")

    reconciliations_sorted = sorted(
        reconciliations,
        key=lambda r: (date_sort_key(r.get("date")), r.get("check", "")),
    )

    recon_rows = "".join(
        f"<tr>"
        f"<td>{r['check']}</td>"
        f"<td class='nowrap'>{normalize_date(r.get('date'))}</td>"
        f"<td><span class='tag tag-{r['source_a']}'>{r['label_a']}</span><br><span class='num'>{fmt_val(r.get('value_a'), r.get('unit',''))}</span></td>"
        f"<td><span class='tag tag-{r['source_b']}'>{r['label_b']}</span><br><span class='num'>{fmt_val(r.get('value_b'), r.get('unit',''))}</span></td>"
        f"<td class='num {status_class(r.get('status',''))}'>{fmt_val(r.get('variance'), r.get('unit','')) if r.get('variance') is not None else '—'}</td>"
        f"<td class='{status_class(r.get('status',''))}'>{r.get('status','').upper()}</td>"
        f"</tr>"
        for r in reconciliations_sorted
    )

    trading_day = daily.get("batch_date", "—")
    trading_batch = daily.get("batch_number", "—")
    report_time = daily.get("report_generated", "—")
    eft_date = normalize_date(eft.get("batch_date") or trading_day)
    stock_date = normalize_date(stock.get("stock_take_date") or "—")

    timeline = build_daily_timeline(history, ocr)
    timeline_rows = ""
    for row in timeline:
        is_latest = row.get("date_display") == normalize_date(trading_day)
        tr_cls = "latest-day" if is_latest else ""
        cv = row.get("cash_variance")
        cv_cls = "warn" if cv is not None and abs(cv) > 50 else ""
        timeline_rows += (
            f"<tr class='{tr_cls}'>"
            f"<td class='nowrap'><strong>{row.get('date_display', '—')}</strong>"
            f"{' <span class=\"tag-latest\">Latest</span>' if is_latest else ''}</td>"
            f"<td>{('B' + str(row['batch'])) if row.get('batch') else '—'}</td>"
            f"<td class='num'>{fmt_zar(row['nett_takings']) if row.get('nett_takings') is not None else '—'}</td>"
            f"<td class='num {delta_class_from_change(row.get('delta_nett'))}'>{fmt_signed_delta(row.get('delta_nett'))}</td>"
            f"<td class='num'>{fmt_litres(row.get('fuel_volume') or row.get('ocr_fuel_litres')) if (row.get('fuel_volume') or row.get('ocr_fuel_litres')) else '—'}</td>"
            f"<td class='num {delta_class_from_change(row.get('delta_fuel_l'))}'>{fmt_signed_delta(row.get('delta_fuel_l'), 'L')}</td>"
            f"<td class='num'>{fmt_zar(row['shop_total']) if row.get('shop_total') is not None else '—'}</td>"
            f"<td class='num {cv_cls}'>{fmt_zar(cv) if cv is not None else '—'}</td>"
            f"<td class='num'>{fmt_zar(row['cit_pickup']) if row.get('cit_pickup') else '—'}</td>"
            f"</tr>"
        )

    latest_atg = ocr.get("atg_dips", [])[-1] if ocr.get("atg_dips") else None
    atg_rows = ""
    if latest_atg:
        atg_rows = "".join(
            f"<tr><td>{p['product']}</td><td class='num'>{p['litres']:,.0f} L</td>"
            f"<td class='num'>{p['available']:,.0f} L</td></tr>"
            for p in latest_atg.get("products", [])
        )
    days_rows = "".join(
        f"<tr><td>{d['product']}</td><td class='num'>{d['avg_daily_litres']:,.0f} L/day</td>"
        f"<td class='num {'warn' if d.get('below_threshold') else ''}'>{d['days_stock_24may']:.1f} days</td></tr>"
        for d in ocr.get("days_of_stock", [])
    )
    ocr_fuel_rows = "".join(
        f"<tr><td class='nowrap'>{normalize_date(f['date'])}</td><td class='num'>{f['ulp95']:,.1f}</td>"
        f"<td class='num'>{f['ulp93']:,.1f}</td><td class='num'>{f['diesel']:,.1f}</td>"
        f"<td class='num'>{fmt_litres(f['total_litres'])}</td></tr>"
        for f in ocr.get("fuel_volume_daily", [])
    )
    ocr_pump_rows = "".join(
        f"<tr><td>B{r['batch']}</td><td class='nowrap'>{normalize_date(r['date'])}</td>"
        f"<td class='num'>{r['pump_litres']:,.1f} L</td><td class='num'>{r['tank_litres']:,.0f} L</td>"
        f"<td class='num {status_class(r['status'])}'>{r['variance_litres']:+.2f} L</td>"
        f"<td class='{status_class(r['status'])}'>{r['status'].upper()}</td></tr>"
        for r in ocr.get("pump_tank_eod", [])
    )
    cit_rows = "".join(
        f"<tr><td class='nowrap'>{normalize_date(c['date'])}</td><td>{c.get('type','cit_pickup')}</td>"
        f"<td class='num'>{fmt_zar(c['amount'])}</td></tr>"
        for c in ocr.get("cit_pickups", [])
    )
    alert_items = "".join(
        f"<li class='{'warn' if 'low' in a.get('type','') or 'delivery' in a.get('type','') else ''}'>{a.get('message', a.get('type',''))}</li>"
        for a in ocr.get("alerts", [])
    )
    staff_rows = "".join(
        f"<tr><td>{s['operator']}</td><td class='nowrap'>{normalize_date(s['date'])}</td>"
        f"<td class='num warn'>{fmt_zar(s['variance'])} over</td><td>{s['status']}</td></tr>"
        for s in ocr.get("staff_exceptions", [])
    )

    payroll_section = ""
    if payroll_runs:
        latest = payroll_runs[0]
        payroll_rows = "".join(
            f"<tr><td>{e['code']}</td><td>{e['name']}</td><td class='num'>{fmt_zar(e['net_pay'])}</td></tr>"
            for e in latest.get("employees", [])
        )
        excluded_count = latest.get("excluded_employee_count", 0)
        excluded_total = latest.get("excluded_total_net_pay", 0)
        all_runs = "".join(
            f"<li><strong>{r['source_file']}</strong> — {normalize_date(r['pay_date'])} — "
            f"{r['employee_count']} ACB staff — {fmt_zar(r['total_net_pay'])} — "
            f"{r.get('excluded_employee_count', 0)} excluded — "
            f"<code>{Path(r['output']).name}</code></li>"
            for r in payroll_runs
        )
        payroll_section = f"""
  <section class="card">
    {h2(f"Payroll — latest {normalize_date(latest.get('pay_date', ''))}", 'payroll', 'payroll_system')}
    <div class="kpi-row">
      <div class="kpi"><span class="label">ACB Employees</span><span class="value">{latest['employee_count']}</span></div>
      <div class="kpi"><span class="label">ACB Payment Total</span><span class="value">{fmt_zar(latest['total_net_pay'])}</span></div>
      <div class="kpi"><span class="label">Excluded Non-ACB</span><span class="value {'warn' if excluded_count else ''}">{excluded_count}</span><span class="label">{fmt_zar(excluded_total)}</span></div>
      <div class="kpi"><span class="label">CSV Ready</span><span class="value small">{Path(latest['output']).name}</span></div>
    </div>
    <table><thead><tr><th>Code</th><th>Name</th><th class="num">Net Pay</th></tr></thead>
    <tbody>{payroll_rows}</tbody></table>
    <p class="note"><strong>All payroll runs tested:</strong></p><ul class="runs">{all_runs}</ul>
  </section>"""

    bank_section = ""
    if bank:
        wage_rows = "".join(
            f"<tr><td>{normalize_date(w['date'])}</td><td class='num'>{w['employee_count']}</td>"
            f"<td class='num'>{fmt_zar(w['total'])}</td></tr>"
            for w in bank.get("wage_runs", [])[:6]
        )
        sp_rows = "".join(
            f"<tr><td>{normalize_date(r['date'])}</td><td class='num'>{fmt_zar(r['total'])}</td></tr>"
            for r in bank.get("speedpoint_daily", [])[-10:]
        )
        cats = bank.get("by_category", {})
        bank_section = f"""
  <section class="card">
    {h2(f"Bank Statement — {bank.get('period_start','')} to {bank.get('period_end','')}", 'bank_statement', 'bank_feed')}
    <div class="kpi-row">
      <div class="kpi"><span class="label">Account</span><span class="value">{bank.get('account_id','')}</span></div>
      <div class="kpi"><span class="label">Ledger Balance</span><span class="value ok">{fmt_zar(bank.get('ledger_balance') or 0)}</span></div>
      <div class="kpi"><span class="label">Speedpoint In</span><span class="value ok">{fmt_zar(cats.get('speedpoint', 0))}</span></div>
      <div class="kpi"><span class="label">Wages Out</span><span class="value">{fmt_zar(abs(cats.get('wages', 0)))}</span></div>
      <div class="kpi"><span class="label">Transactions</span><span class="value">{bank.get('transaction_count',0)}</span></div>
    </div>
    <p class="note">Source: FNB OFX · <code>{bank.get('source_file', '')}</code> · Balance as of {normalize_date(bank.get('ledger_balance_date', ''))}</p>
    <div class="grid" style="margin-top:1rem">
      <div>
        <h3 style="font-size:.85rem;margin:0 0 .5rem">Recent wage runs (bank debits)</h3>
        <table><thead><tr><th>Posted</th><th class="num">Lines</th><th class="num">Total</th></tr></thead>
        <tbody>{wage_rows or '<tr><td colspan="3">—</td></tr>'}</tbody></table>
      </div>
      <div>
        <h3 style="font-size:.85rem;margin:0 0 .5rem">Speedpoint credits (last 10 days)</h3>
        <table><thead><tr><th>Posted</th><th class="num">Credit</th></tr></thead>
        <tbody>{sp_rows or '<tr><td colspan="2">—</td></tr>'}</tbody></table>
      </div>
    </div>
  </section>"""

    supplier_section = ""
    if supplier and supplier.get("invoice_count"):
        dept_rows = "".join(
            f"<tr><td>{d}</td><td class='num'>{fmt_zar(v)}</td></tr>"
            for d, v in supplier.get("by_department", {}).items()
        )
        supplier_section = f"""
  <section class="card">
    {h2('Supplier Invoices (Schedule of Accounts)', 'supplier_schedule', 'manual_recon')}
    <div class="kpi-row">
      <div class="kpi"><span class="label">Invoices</span><span class="value">{supplier['invoice_count']}</span></div>
      <div class="kpi"><span class="label">Total Incl VAT</span><span class="value">{fmt_zar(supplier['total_incl'])}</span></div>
    </div>
    <table><thead><tr><th>Department</th><th class="num">Spend</th></tr></thead><tbody>{dept_rows}</tbody></table>
  </section>"""

    ap_workflow_rows = "".join([
        f"<tr><td>Supplier account schedule</td><td>{'Loaded' if supplier else 'Pending file'}</td><td><code>supplier_schedule</code></td></tr>",
        f"<tr><td>Supplier invoice / creditors detail</td><td>{'Classified' if 'creditors_purchases_detail' in repo_type_ids else 'Pending sample'}</td><td><code>creditors_purchases_detail</code></td></tr>",
        f"<tr><td>Bank payment verification</td><td>{'Loaded' if bank else 'Pending OFX'}</td><td><code>bank_statement</code></td></tr>",
        f"<tr><td>Payroll payment file</td><td>{'Generated' if payroll_runs else 'Pending Nett Pay List'}</td><td><code>payment_csv</code></td></tr>",
    ])
    ap_workflow_section = f"""
  <section class="card">
    {h2('Agent AP / Payroll Workflow Status', 'reconciliation_matrix')}
    <p class="note">Agent OS contract: email, OneDrive, or manual uploads land under <code>docs/_ai_context/inputs/</code>, then <code>scripts/management/refresh_all.py</code> classifies, reconciles where parsers exist, and refreshes the dashboard. Invoice matching remains human-review until real invoice samples validate the parser.</p>
    <table><thead><tr><th>Workflow input</th><th>Status</th><th>Report contract</th></tr></thead><tbody>{ap_workflow_rows}</tbody></table>
  </section>"""

    cash_up_section = ""
    if cash_up:
        sheets = ", ".join(cash_up.get("sheet_names", [])[:6])
        cash_up_section = f"""
  <section class="card">
    {h2('Cash Up Workbook', 'cash_up', 'manual_recon')}
    <div class="kpi-row">
      <div class="kpi"><span class="label">File</span><span class="value small">{cash_up.get('source_file', '')}</span></div>
      <div class="kpi"><span class="label">Sheets</span><span class="value">{cash_up.get('sheet_count', 0)}</span></div>
    </div>
    <p class="note">{cash_up.get('site_title') or 'Manual month-end cash reconciliation workbook.'} Tabs: {sheets or '—'}</p>
  </section>"""

    cash_class = "warn" if abs(daily.get("cash_variance", 0)) > 50 else "ok"

    ocr_section = ""
    if ocr:
        atg_date_label = normalize_date(latest_atg.get("date", "—")) if latest_atg else "—"
        ocr_section = f"""
  <section class="card">
    {h2(f"ATG Tank Levels ({atg_date_label})", 'atg_tank_levels', 'ocr_whatsapp')}
    <p class="note">Source: {ocr.get('channel', 'WhatsApp OCR')} · File: {ocr.get('source_file', '')}</p>
    <table><thead><tr><th>Product</th><th class="num">In Tank</th><th class="num">Available</th></tr></thead>
    <tbody>{atg_rows or '<tr><td colspan="3">No ATG data</td></tr>'}</tbody></table>
    <h3 style="font-size:.85rem;margin:1rem 0 .5rem">Days of Stock (24 May)</h3>
    <table><thead><tr><th>Product</th><th class="num">Avg Daily</th><th class="num">Days Left</th></tr></thead>
    <tbody>{days_rows or '<tr><td colspan="3">—</td></tr>'}</tbody></table>
  </section>

  <section class="card">
    {h2('OCR Fuel Volume & Wet Stock (WhatsApp)', 'ocr_fuel_trend', 'ocr_whatsapp')}
    <table><thead><tr><th>Date</th><th class="num">ULP95</th><th class="num">ULP93</th><th class="num">Diesel</th><th class="num">Total</th></tr></thead>
    <tbody>{ocr_fuel_rows or '<tr><td colspan="5">No data</td></tr>'}</tbody></table>
    <h3 style="font-size:.85rem;margin:1rem 0 .5rem">Pump vs Tank (from OCR images)</h3>
    <table><thead><tr><th>Batch</th><th>Date</th><th class="num">Pump</th><th class="num">Tank</th><th class="num">Variance</th><th>Status</th></tr></thead>
    <tbody>{ocr_pump_rows or '<tr><td colspan="6">No data</td></tr>'}</tbody></table>
  </section>

  <section class="grid">
    <div class="card">{h2('CIT Cash Pickups', 'cit_pickups', 'ocr_whatsapp')}
      <table><thead><tr><th>Date</th><th>Type</th><th class="num">Amount</th></tr></thead>
      <tbody>{cit_rows or '<tr><td colspan="3">No data</td></tr>'}</tbody></table>
    </div>
    <div class="card">{h2('Operational Alerts', 'operational_alerts', 'ocr_whatsapp')}
      <ul class="runs">{alert_items or '<li>No active alerts</li>'}</ul>
      {'<h3 style="font-size:.85rem;margin:1rem 0 .5rem">Staff Till Exceptions</h3><table><thead><tr><th>Operator</th><th>Date</th><th class="num">Variance</th><th>Status</th></tr></thead><tbody>' + staff_rows + '</tbody></table>' if staff_rows else ''}
    </div>
  </section>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Management Dashboard — {daily.get('site_name', 'Site')}</title>
  <style>
    body {{ font-family: system-ui, sans-serif; background: #f4f5f7; color: #1a1a1a; max-width: 1100px; margin: 0 auto; padding: 1rem; }}
    h1 {{ font-size: 1.25rem; margin: 0 0 .25rem; }}
    h2 {{ font-size: .95rem; margin: 0 0 .75rem; border-bottom: 1px solid #eee; padding-bottom: .35rem; display: flex; align-items: center; gap: .35rem; }}
    .meta {{ color: #666; font-size: .85rem; margin-bottom: 1rem; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: .75rem; }}
    .card {{ background: #fff; border-radius: 8px; padding: 1rem; box-shadow: 0 1px 3px rgba(0,0,0,.08); margin-bottom: .75rem; }}
    .kpi-row {{ display: flex; flex-wrap: wrap; gap: 1rem; }}
    .kpi .label {{ display: block; font-size: .7rem; text-transform: uppercase; color: #888; }}
    .kpi .value {{ font-size: 1.15rem; font-weight: 600; }}
    .kpi .value.small {{ font-size: .85rem; }}
    table {{ width: 100%; border-collapse: collapse; font-size: .82rem; }}
    th, td {{ padding: .35rem .25rem; border-bottom: 1px solid #f0f0f0; }}
    .num {{ text-align: right; font-variant-numeric: tabular-nums; }}
    .warn {{ color: #c0392b; font-weight: 600; }}
    .ok {{ color: #27ae60; }}
    .note {{ font-size: .75rem; color: #666; margin-top: .5rem; }}
    code {{ background: #eee; padding: .1rem .3rem; border-radius: 3px; }}
    ul.runs {{ font-size: .8rem; margin: .25rem 0 0 1rem; }}
    .tag {{ font-size: .65rem; padding: .1rem .35rem; border-radius: 3px; text-transform: uppercase; }}
    .tag-pos_system {{ background: #dbeafe; color: #1e40af; }}
    .tag-payroll_system {{ background: #fce7f3; color: #9d174d; }}
    .tag-bank_feed {{ background: #d1fae5; color: #065f46; }}
    .tag-manual_recon {{ background: #fef3c7; color: #92400e; }}
    .tag-ocr_whatsapp {{ background: #ede9fe; color: #5b21b6; }}
    .legend {{ display: flex; flex-wrap: wrap; gap: .5rem; margin-bottom: 1rem; font-size: .75rem; }}
    .card-context {{ font-size: .72rem; color: #64748b; margin: -.25rem 0 .65rem; line-height: 1.4; }}
    .report-banner {{ background: #1e293b; color: #f8fafc; padding: .85rem 1rem; border-radius: 8px; margin-bottom: .75rem; }}
    .report-banner strong {{ color: #fff; }}
    .nowrap {{ white-space: nowrap; }}
    .latest-day {{ background: #f0fdf4; }}
    .tag-latest {{ font-size: .6rem; background: #16a34a; color: #fff; padding: .1rem .3rem; border-radius: 3px; margin-left: .25rem; }}
    .up {{ color: #16a34a; }}
    .down {{ color: #dc2626; }}
    .flat {{ color: #64748b; }}
    .tip {{ position: relative; display: inline-flex; cursor: help; }}
    .tip-icon {{ width: 1rem; height: 1rem; border-radius: 50%; background: #64748b; color: #fff; font-size: .65rem; font-weight: 700; display: inline-flex; align-items: center; justify-content: center; }}
    .tip-body {{ display: none; position: absolute; left: 1.25rem; top: -.25rem; z-index: 20; width: min(420px, 85vw); background: #1e293b; color: #f8fafc; padding: .65rem .85rem; border-radius: 6px; font-size: .75rem; font-weight: 400; line-height: 1.5; box-shadow: 0 4px 12px rgba(0,0,0,.2); }}
    .tip:hover .tip-body, .tip:focus .tip-body, .tip:focus-within .tip-body {{ display: block; }}
  </style>
</head>
<body>
  <nav style="background:#1a2332;color:#fff;padding:.6rem 1rem;margin:-1rem -1rem 1rem;display:flex;flex-wrap:wrap;gap:1rem;align-items:center;font-size:.9rem">
    <strong style="color:#fff">Management Report</strong>
    <a href="help/management-dashboard.html" style="color:#90caf9" target="_blank">Help guide</a>
    <a href="file-views/index.html" style="color:#90caf9">File repository (drill-down)</a>
    <a href="../../docs/_ai_context/guides/DATA_INTERPRETATION_GUIDE.md" style="color:#90caf9" target="_blank">Data interpretation</a>
  </nav>
  <h1>{daily.get('site_name', 'Management Dashboard')}</h1>
  <div class="report-banner">
    <strong>Primary trading day:</strong> {normalize_date(trading_day)} · Day End Batch {trading_batch}
    · POS report generated {report_time}
    · Dashboard refreshed {datetime.now().strftime('%d/%m/%Y %H:%M')}
  </div>
  <p class="note">All dates use <strong>DD/MM/YYYY</strong> (South African). KPI cards show which trading day they apply to. The timeline below tracks day-on-day changes.</p>

  <section class="card">
    {h2('Daily Operations Timeline', 'daily_timeline')}
    <p class="note">Chronological story — each row is one trading day. Δ columns show change vs the previous day. Highlighted row = latest POS Day End.</p>
    <table><thead><tr>
      <th>Trading Day</th><th>Batch</th><th class="num">Nett Takings</th><th class="num">Δ Nett</th>
      <th class="num">Fuel (L)</th><th class="num">Δ Fuel</th><th class="num">Shop</th>
      <th class="num">Cash Var</th><th class="num">CIT Pickup</th>
    </tr></thead>
    <tbody>{timeline_rows or '<tr><td colspan="9">Add Day End files to build timeline</td></tr>'}</tbody></table>
  </section>

  <section class="card">
    <h2>Snapshot — {normalize_date(trading_day)} <span class="tag tag-pos_system">POS System</span></h2>
    <p class="card-context">These eight cards summarise the <strong>latest trading day only</strong> (Batch {trading_batch}). EFT and Stock Take may reference different report dates — see each card.</p>
  </section>

  <section class="grid">
    <div class="card">{kpi_context(trading_day, trading_batch)}{h2('Daily Nett Takings', 'nett_takings', 'pos_system')}<div class="kpi"><span class="value">{fmt_zar(daily.get('nett_takings', 0))}</span></div></div>
    <div class="card">{kpi_context(trading_day, trading_batch)}{h2('Fuel Sales', 'fuel_sales', 'pos_system')}<div class="kpi"><span class="value">{fmt_zar(daily.get('fuel_total', 0))}</span><span class="label">{daily.get('fuel_volume', 0):,.2f} L · GP {daily.get('fuel_gp_percent', 0):.1f}%</span></div></div>
    <div class="card">{kpi_context(trading_day, trading_batch)}{h2('Shop Sales', 'shop_sales', 'pos_system')}<div class="kpi"><span class="value">{fmt_zar(daily.get('shop_total_incl', 0))}</span><span class="label">GP {daily.get('shop_gp_percent', 0):.1f}%</span></div></div>
    <div class="card">{kpi_context(trading_day, trading_batch)}{h2('Cash Variance', 'cash_variance', 'pos_system')}<div class="kpi"><span class="value {cash_class}">{fmt_zar(daily.get('cash_variance', 0))}</span><span class="label">Target &lt; R50 · end of shift count</span></div>
  </section>

  <section class="grid">
    <div class="card">{kpi_context(trading_day, trading_batch, 'Customer counts for this trading day')}{h2('Customers', 'fuel_customers', 'pos_system')}
      <div class="kpi-row">
        <div class="kpi"><span class="label">Fuel</span><span class="value">{daily.get('fuel_customers', 0)}</span></div>
        <div class="kpi"><span class="label">Shop</span><span class="value">{daily.get('shop_customers', 0)}</span></div>
      </div>
    </div>
    <div class="card">{kpi_context(eft_date, None, 'Card batch sent to bank on this date — from EFT Batch Summary file')}{h2(f"EFT Batch ({eft_date})", 'eft_batch', 'pos_system')}<div class="kpi"><span class="value">{fmt_zar(eft.get('total_amount', 0))}</span><span class="label">{eft.get('total_trx', 0)} transactions</span></div></div>
    <div class="card">{kpi_context(trading_day, trading_batch, 'Unsent at Day End close')}{h2('EFT Pending', 'eft_pending', 'pos_system')}<div class="kpi"><span class="value">{fmt_zar(pending.get('pending_total', 0))}</span><span class="label">Awaiting next batch</span></div></div>
    <div class="card">{kpi_context(stock_date, note='Stock take report date — may differ from latest trading day')}{h2(f"Stock Take ({stock_date})", 'stock_take', 'pos_system')}<div class="kpi"><span class="value">{stock.get('sku_variances', 0)} SKUs</span><span class="label">@ cost {fmt_zar(stock.get('variance_value_at_cost', 0))}</span></div>
  </section>

  <section class="card">
    {h2('Data Source Legend', 'source_legend')}
    <div class="legend">{src_badge('pos_system')} {src_badge('bank_feed')} {src_badge('payroll_system')} {src_badge('manual_recon')} {src_badge('ocr_whatsapp')}</div>
    <p class="note">Each section is tagged with its primary source. Purple OCR data comes from WhatsApp photos — confirm against POS or bank when making decisions.</p>
  </section>

  <section class="card">
    {h2('Multi-Source Reconciliation', 'reconciliation_matrix')}
    <p class="note">Sorted chronologically · all dates DD/MM/YYYY · compares Source A vs Source B</p>
    <table><thead><tr><th>Check</th><th>Trading Day</th><th>Source A</th><th>Source B</th><th class="num">Variance</th><th>Status</th></tr></thead>
    <tbody>{recon_rows or '<tr><td colspan="6">No comparisons yet</td></tr>'}</tbody></table>
  </section>

  <section class="card">
    {h2(f"Wet Stock EOD — {normalize_date(trading_day)}", 'wet_stock', 'pos_system')}
    <table><thead><tr><th>Grade</th><th class="num">Pump Vol</th><th class="num">Sales</th><th class="num">Variance</th></tr></thead>
    <tbody>{grade_rows or '<tr><td colspan="4">No data</td></tr>'}</tbody></table>
    <p class="note">Pump vs tank variance total: {fuel_var_total:+.2f} L</p>
  </section>

  <section class="grid">
    <div class="card">{h2('Top Shop Categories', 'top_categories', 'pos_system')}
      <table><thead><tr><th>Cat</th><th class="num">Sales</th><th class="num">GP%</th></tr></thead><tbody>{cat_rows}</tbody></table>
    </div>
    <div class="card">{h2('MTD Fuel Variance % (May)', 'mtd_fuel_variance', 'pos_system')}
      <table><thead><tr><th>Grade</th><th class="num">MTD %</th></tr></thead><tbody>{mtd_var_rows or '<tr><td colspan="2">—</td></tr>'}</tbody></table>
    </div>
  </section>

  <section class="card">
    {h2('Cashier EOS Exceptions', 'cashiers', 'pos_system')}
    <table><thead><tr><th>Cashier</th><th class="num">Nett Takings</th><th class="num">Voids</th><th class="num">Void Amt</th></tr></thead>
    <tbody>{cashier_rows or '<tr><td colspan="4">No data</td></tr>'}</tbody></table>
  </section>

  <section class="card">
    {h2(f"Monthly Reference — {monthly.get('period', 'April 2026')}", 'monthly_reference', 'pos_system')}
    <div class="kpi-row">
      <div class="kpi"><span class="label">Nett Takings</span><span class="value">{fmt_zar(monthly.get('nett_takings', 0))}</span></div>
      <div class="kpi"><span class="label">Combined Sales</span><span class="value">{fmt_zar(monthly.get('combined_sales', 0))}</span></div>
      <div class="kpi"><span class="label">Fuel Volume</span><span class="value">{monthly.get('fuel_volume', 0):,.0f} L</span></div>
      <div class="kpi"><span class="label">Banking Var</span><span class="value warn">{fmt_zar(monthly.get('cash_variance_banking', 0))}</span></div>
    </div>
  </section>

  {bank_section}
  {supplier_section}
  {ap_workflow_section}
  {cash_up_section}
  {ocr_section}

  <section class="card">
    {h2('Daily History', 'daily_history', 'pos_system')}
    <table><thead><tr><th>Date</th><th>Batch</th><th class="num">Nett Takings</th><th class="num">Cash Var</th></tr></thead>
    <tbody>{hist_rows or '<tr><td colspan="4">Add Day End files</td></tr>'}</tbody></table>
  </section>

  {payroll_section}

  {file_repo_section}

  <section class="card">
    {h2('Input File Registry', 'input_registry')}
    <p class="note">Each file is classified by source type for future reconciliation workflows.</p>
    <table><thead><tr><th>Source</th><th>File</th><th>Report</th><th>Modified</th></tr></thead>
    <tbody>{inv_rows or '<tr><td colspan="4">No files scanned</td></tr>'}</tbody></table>
  </section>

  <p class="meta">Refresh: <code>python scripts/management/generate_dashboard.py</code> · Payroll only: <code>python scripts/payroll/netpay_to_payment_csv.py --all</code></p>
</body>
</html>"""


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs", default="docs/_ai_context/inputs/Starter Docs")
    parser.add_argument("--json", default="reports/data/canonical-latest.json")
    parser.add_argument("--html", default="reports/management-dashboard.html")
    parser.add_argument("--skip-payroll", action="store_true")
    args = parser.parse_args()

    inputs = ROOT / args.inputs
    json_path = ROOT / args.json
    html_path = ROOT / args.html

    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "management" / "build_file_repo.py")],
        check=True,
        cwd=str(ROOT),
    )
    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "management" / "generate_file_views.py")],
        check=True,
        cwd=str(ROOT),
    )
    data = run_parsers(inputs, json_path)
    payroll_runs = [] if args.skip_payroll else run_all_payroll()
    if payroll_runs:
        payroll_path = ROOT / "reports" / "data" / "payroll-latest.json"
        payroll_path.parent.mkdir(parents=True, exist_ok=True)
        payroll_path.write_text(json.dumps(payroll_runs, indent=2), encoding="utf-8")

    file_repo = load_file_repo_index()
    html_path.parent.mkdir(parents=True, exist_ok=True)
    html_path.write_text(build_html(data, payroll_runs, file_repo), encoding="utf-8")
    print(f"Dashboard: {html_path}")
    print(f"Canonical: {json_path}")
    if payroll_runs:
        for r in payroll_runs:
            print(f"Payroll: {r['source_file']} -> {Path(r['output']).name} ({fmt_zar(r['total_net_pay'])})")


if __name__ == "__main__":
    main()
