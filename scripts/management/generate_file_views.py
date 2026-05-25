#!/usr/bin/env python3
"""Generate file-level drill-down HTML pages and help guides (Phase 2)."""

from __future__ import annotations

import html
import json
import re
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "reports" / "data"
VIEWS = ROOT / "reports" / "file-views"
HELP = ROOT / "reports" / "help"
ASSETS = ROOT / "reports" / "assets"

sys_path = ROOT / "scripts" / "management"
import sys

sys.path.insert(0, str(sys_path))
from catalog_loader import frequency_label, get_report_spec, load_catalog  # noqa: E402
from format_utils import normalize_date  # noqa: E402


def esc(s: Any) -> str:
    return html.escape(str(s)) if s is not None else ""


def fmt_zar(n: float | None) -> str:
    if n is None:
        return "—"
    return f"R {n:,.2f}"


def src_tag(source_type: str) -> str:
    return f'<span class="tag tag-{esc(source_type)}">{esc(source_type.replace("_", " ").title())}</span>'


def parser_badge(status: str) -> str:
    cls = {"integrated": "badge-integrated", "integrated_partial": "badge-integrated",
           "integrated_summary_only": "badge-integrated", "classified_only": "badge-pending",
           "metadata_only": "badge-pending", "not_implemented": "badge-none",
           "output_artifact": "badge-integrated"}.get(status, "badge-none")
    return f'<span class="{cls}">{esc(status.replace("_", " "))}</span>'


def md_to_html_simple(text: str) -> str:
    lines = text.splitlines()
    out: list[str] = []
    in_table = False
    for line in lines:
        if line.startswith("---"):
            continue
        if line.startswith("# "):
            out.append(f"<h1>{esc(line[2:])}</h1>")
        elif line.startswith("## "):
            out.append(f"<h2>{esc(line[3:])}</h2>")
        elif line.startswith("### "):
            out.append(f"<h3>{esc(line[4:])}</h3>")
        elif line.startswith("|") and "|" in line[1:]:
            if not in_table:
                out.append("<table>")
                in_table = True
            if re.match(r"^\|[\s\-:|]+\|$", line):
                continue
            cells = [c.strip() for c in line.strip("|").split("|")]
            out.append("<tr>" + "".join(f"<td>{esc(c)}</td>" for c in cells) + "</tr>")
        else:
            if in_table:
                out.append("</table>")
                in_table = False
            if line.strip().startswith("- "):
                if out and not out[-1].endswith("</ul>"):
                    if "<ul>" not in out[-1]:
                        out.append("<ul>")
                out.append(f"<li>{esc(line.strip()[2:])}</li>")
            elif line.strip():
                out.append(f"<p>{esc(line)}</p>")
            elif out and out[-1].startswith("<li>"):
                out.append("</ul>")
    if in_table:
        out.append("</table>")
    return "\n".join(out)


def help_panel_html(spec: dict[str, Any], report_type: str) -> str:
    if not spec:
        return "<p>No catalog entry for this report type.</p>"
    fields = spec.get("key_fields") or []
    insights = spec.get("valuable_insights") or []
    callouts = spec.get("owner_callouts") or []
    lines = [
        f"<h3>{esc(spec.get('pattern_names', [report_type])[0] if spec.get('pattern_names') else report_type)}</h3>",
        f"<p><strong>Frequency:</strong> {esc(frequency_label(spec.get('frequency', '')))} · "
        f"<strong>Parser:</strong> {parser_badge(spec.get('parser_status', 'unknown'))}</p>",
        f"<p>{esc(spec.get('business_purpose', ''))}</p>",
    ]
    if fields:
        lines.append("<dl><dt>Key fields</dt><dd><ul>")
        lines.extend(f"<li><code>{esc(f)}</code></li>" for f in fields)
        lines.append("</ul></dd></dl>")
    if insights:
        lines.append("<dl><dt>Valuable insights</dt><dd><ul>")
        lines.extend(f"<li>{esc(i)}</li>" for i in insights)
        lines.append("</ul></dd></dl>")
    if callouts:
        lines.append("<div class='callout'><strong>Owner callouts</strong><ul>")
        lines.extend(f"<li>{esc(c)}</li>" for c in callouts)
        lines.append("</ul></div>")
    recon = spec.get("reconciles_with")
    if recon:
        lines.append(f"<p><strong>Reconciles with:</strong> {esc(', '.join(recon))}</p>")
    return "\n".join(lines)


def period_label(summary: dict[str, Any]) -> str:
    for k in ("batch_date", "period_end", "period_start", "pay_date", "stock_take_date", "batch_date"):
        if summary.get(k):
            return normalize_date(str(summary[k]))
    return "—"


def fmt_metric(key: str, val: float) -> str:
    if "volume" in key or "litres" in key:
        return f"{val:,.2f} L"
    if "trx" in key or key.endswith("_count") or key == "sku_variances":
        return f"{int(val):,}"
    if any(x in key for x in ("total", "nett", "amount", "balance", "variance", "pay", "credit", "debit", "pending", "incl", "cost")):
        return fmt_zar(val)
    return f"{val:,.2f}"


def trend_rows(points: list[dict], metric_keys: list[str]) -> str:
    if not points:
        return "<tr><td colspan='99'>No series points — upload files and run build_file_repo.py</td></tr>"
    rows: list[str] = []
    prev: dict[str, float] = {}
    for pt in points:
        s = pt.get("summary", {})
        period = period_label(s)
        cells = [f"<td class='nowrap'><strong>{esc(period)}</strong></td>"]
        cells.append(f"<td>B{esc(s['batch'])}</td>" if s.get("batch") else "<td>—</td>")
        for key in metric_keys:
            val = s.get(key)
            if isinstance(val, (int, float)):
                fv = float(val)
                delta = ""
                if key in prev:
                    d = fv - prev[key]
                    cls = "up" if d > 0 else "down" if d < 0 else ""
                    delta = f" <span class='{cls}'>({d:+,.2f})</span>"
                cells.append(f"<td class='num'>{fmt_metric(key, fv)}{delta}</td>")
                prev[key] = fv
            else:
                cells.append(f"<td>{esc(val)}</td>")
        cells.append(f"<td><code>{esc(pt.get('source_file', ''))}</code></td>")
        rows.append(f"<tr class='clickable' data-path='{esc(pt.get('path', ''))}'>{''.join(cells)}</tr>")
    return "\n".join(rows)


def default_metrics(report_type: str) -> list[str]:
    return {
        "day_end_summary": ["nett_takings", "fuel_volume", "cash_variance", "shop_total_incl"],
        "eft_batch_summary": ["total_amount", "total_trx"],
        "eft_pending": ["pending_total"],
        "bank_statement": ["ledger_balance", "total_credits", "total_debits"],
        "nett_pay_list": ["total_net_pay"],
        "stock_take_variance": ["sku_variances", "variance_value_at_cost"],
    }.get(report_type, [])


def ledger_table_rows(entries: list[dict]) -> str:
    if not entries:
        return "<tr><td colspan='6'>No files ingested for this type</td></tr>"
    return "".join(
        f"<tr class='clickable' data-path='{esc(e['path'])}' data-ingest='{esc(e.get('ingest_id', ''))}'>"
        f"<td><code>{esc(e['filename'])}</code></td>"
        f"<td>{esc(e.get('folder', ''))}</td>"
        f"<td class='nowrap'>{esc(e.get('content_key', ''))}</td>"
        f"<td>{'dup' if e.get('is_duplicate_copy') else 'primary'}</td>"
        f"<td>{esc(e.get('modified', ''))}</td>"
        f"<td class='num'>{e.get('size_bytes', 0):,}</td></tr>"
        for e in sorted(entries, key=lambda x: x.get("modified", ""), reverse=True)
    )


def build_type_page(
    report_type: str,
    spec: dict[str, Any],
    series: dict,
    ledger_entries: list[dict],
    catalog: dict,
) -> str:
    points = series.get("points", [])
    source_type = spec.get("source_type", ledger_entries[0]["source_type"] if ledger_entries else "unknown")
    metrics = default_metrics(report_type)
    metric_headers = "".join(f"<th class='num'>{esc(m.replace('_', ' ').title())}</th>" for m in metrics)
    ledger_json = json.dumps(ledger_entries, indent=2)
    points_json = json.dumps(points, indent=2)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <title>{esc(report_type)} — File View</title>
  <link rel="stylesheet" href="../assets/site.css"/>
</head>
<body>
  <nav class="top-nav">
    <a href="../management-dashboard.html">Management Report</a>
    <a href="index.html">File Repository</a>
    <strong>{esc(report_type)}</strong>
  </nav>
  <div class="wrap">
    <div class="card">
      <h1>{esc(spec.get('pattern_names', [report_type])[0] if spec.get('pattern_names') else report_type)}</h1>
      <p class="meta">{src_tag(source_type)}
        Frequency: <strong>{esc(frequency_label(spec.get('frequency', '')))}</strong> ·
        {parser_badge(spec.get('parser_status', 'unknown'))} ·
        {len(points)} period(s) in series · {len(ledger_entries)} file(s) on disk
      </p>
      <div class="toolbar">
        <button type="button" class="btn btn-primary" onclick="toggleHelp()">Help — what is this file?</button>
        <a class="btn" href="../help/{report_type}.html" target="_blank">Full help page</a>
        <a class="btn" href="../../docs/_ai_context/knowledge/reference/file-type-catalog.yaml" target="_blank">YAML spec</a>
      </div>
      <div id="helpPanel" class="help-panel">{help_panel_html(spec, report_type)}</div>
    </div>

    <div class="card">
      <h2>Historic trend ({esc(frequency_label(spec.get('frequency', 'daily')))})</h2>
      <p class="meta">One row per business period (batch/date). Parentheses show change vs previous row. Click a row to inspect that file.</p>
      <table id="trendTable">
        <thead><tr><th>Period</th><th>Batch</th>{metric_headers}<th>Source file</th></tr></thead>
        <tbody>{trend_rows(points, metrics)}</tbody>
      </table>
    </div>

    <div class="card">
      <h2>All physical files loaded</h2>
      <p class="meta">Every drop in inputs/ for this report type — includes duplicate copies marked (1).</p>
      <table id="filesTable">
        <thead><tr><th>Filename</th><th>Folder</th><th>Content key</th><th>Role</th><th>Modified</th><th class="num">Size</th></tr></thead>
        <tbody>{ledger_table_rows(ledger_entries)}</tbody>
      </table>
    </div>

    <div id="fileDetail" class="file-detail" style="display:none">
      <h3>File detail</h3>
      <p id="fileMeta" class="meta"></p>
      <pre id="fileJson" class="json"></pre>
    </div>
  </div>
  <script>
    const LEDGER = {ledger_json};
    const SERIES = {points_json};
    function toggleHelp() {{
      document.getElementById('helpPanel').classList.toggle('open');
    }}
    function showFile(path) {{
      const row = LEDGER.find(e => e.path === path) || SERIES.find(p => p.path === path);
      if (!row) return;
      const el = document.getElementById('fileDetail');
      el.style.display = 'block';
      document.getElementById('fileMeta').textContent = row.path + ' · modified ' + (row.modified || '');
      document.getElementById('fileJson').textContent = JSON.stringify(row.summary || row, null, 2);
      el.scrollIntoView({{ behavior: 'smooth', block: 'nearest' }});
    }}
    document.querySelectorAll('tr.clickable').forEach(tr => {{
      tr.addEventListener('click', () => {{
        document.querySelectorAll('tr.selected').forEach(r => r.classList.remove('selected'));
        tr.classList.add('selected');
        showFile(tr.dataset.path);
      }});
    }});
  </script>
</body>
</html>"""


def build_index(index: dict, catalog: dict) -> str:
    rows = "".join(
        f"<tr><td><a href='{esc(t['report_type'])}.html'><code>{esc(t['report_type'])}</code></a></td>"
        f"<td>{src_tag(t.get('source_type', ''))}</td>"
        f"<td>{esc(t.get('pattern_name', ''))}</td>"
        f"<td class='num'>{t.get('series_points', 0)}</td>"
        f"<td class='num'>{t.get('primary_count', 0)}</td>"
        f"<td>{parser_badge(catalog.get(t['report_type'], {}).get('parser_status', 'unknown'))}</td></tr>"
        for t in index.get("report_types", [])
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <title>File Repository — Report Types</title>
  <link rel="stylesheet" href="../assets/site.css"/>
</head>
<body>
  <nav class="top-nav">
    <a href="../management-dashboard.html">Management Report</a>
    <strong>File Repository</strong>
  </nav>
  <div class="wrap">
    <div class="card">
      <h1>File Repository</h1>
      <p class="meta">Drill into each report type for history, trends, callouts, and per-file datasets.
        Generated {esc(index.get('generated_at', ''))}.</p>
      <div class="toolbar">
        <a class="btn btn-primary" href="../help/management-dashboard.html">Management report help</a>
        <a class="btn" href="../../docs/_ai_context/guides/DATA_INTERPRETATION_GUIDE.md" target="_blank">Interpretation guide</a>
      </div>
    </div>
    <div class="card">
      <table>
        <thead><tr><th>Report type</th><th>Source</th><th>Pattern</th><th class="num">Series</th><th class="num">Files</th><th>Parser</th></tr></thead>
        <tbody>{rows}</tbody>
      </table>
    </div>
  </div>
</body>
</html>"""


def build_help_pages(catalog: dict) -> None:
    HELP.mkdir(parents=True, exist_ok=True)
    dash_spec = ROOT / "docs" / "_ai_context" / "knowledge" / "MANAGEMENT_DASHBOARD_SPECIFICATION.md"
    dash_body = md_to_html_simple(dash_spec.read_text(encoding="utf-8")) if dash_spec.exists() else ""
    (HELP / "management-dashboard.html").write_text(
        f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"/><title>Help — Management Dashboard</title>
<link rel="stylesheet" href="../assets/site.css"/></head>
<body>
<nav class="top-nav"><a href="../management-dashboard.html">← Dashboard</a><strong>Help</strong></nav>
<div class="wrap"><div class="card">{dash_body}
<p class="meta">Source: MANAGEMENT_DASHBOARD_SPECIFICATION.md</p></div></div>
</body></html>""",
        encoding="utf-8",
    )
    for report_type, spec in catalog.items():
        body = help_panel_html(spec, report_type)
        (HELP / f"{report_type}.html").write_text(
            f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"/><title>Help — {esc(report_type)}</title>
<link rel="stylesheet" href="../assets/site.css"/></head>
<body>
<nav class="top-nav">
  <a href="../management-dashboard.html">Dashboard</a>
  <a href="../file-views/{report_type}.html">Dataset</a>
  <strong>Help</strong>
</nav>
<div class="wrap"><div class="card">{body}
<p class="meta">Catalog: file-type-catalog.yaml#{esc(report_type)}</p></div></div>
</body></html>""",
            encoding="utf-8",
        )


def main() -> None:
    catalog = load_catalog()
    index = json.loads((DATA / "file-repo-index.json").read_text(encoding="utf-8"))
    ledger = json.loads((DATA / "ingest-ledger.json").read_text(encoding="utf-8"))["entries"]

    VIEWS.mkdir(parents=True, exist_ok=True)
    by_type_ledger: dict[str, list] = {}
    for e in ledger:
        by_type_ledger.setdefault(e["report_type"], []).append(e)

    for report_type in sorted({t["report_type"] for t in index.get("report_types", [])}):
        series_path = DATA / "series" / f"{report_type.replace('/', '_')}.json"
        series = json.loads(series_path.read_text(encoding="utf-8")) if series_path.exists() else {"points": []}
        spec = catalog.get(report_type, get_report_spec(report_type))
        page = build_type_page(report_type, spec, series, by_type_ledger.get(report_type, []), catalog)
        (VIEWS / f"{report_type}.html").write_text(page, encoding="utf-8")

    (VIEWS / "index.html").write_text(build_index(index, catalog), encoding="utf-8")
    build_help_pages(catalog)
    print(f"File views: {VIEWS}/ ({len(list(VIEWS.glob('*.html')))} pages)")
    print(f"Help guides: {HELP}/")


if __name__ == "__main__":
    main()
