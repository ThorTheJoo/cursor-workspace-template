---
document_type: PROMPT
status: ACTIVE
purpose: Agent OS operating guide for Experiment JP reporting and payment workflows
traceability_id: "AGENT-OS-HANDOFF-2026-06-08"
---

# Agent OS Handoff — Experiment JP

This guide is for Hermes Desktop, Open Claw, or a similar agent operating system running this repository in a local workspace.

## Mission

Maintain the Experiment JP reporting workspace by ingesting files from email, OneDrive, or manual upload, classifying them into known report contracts, refreshing generated data, and surfacing management dashboard updates.

The agent must not invent financial matches. If a parser or sample-backed reconciliation does not exist, mark the workflow as `pending` or `human_review_required`.

## Required Context Load

Before acting, read these files in order:

1. `docs/_ai_context/state/repo-manifest.json`
2. `docs/_ai_context/prompts/phases/CONTEXT_MANIFEST.md`
3. `docs/_ai_context/state/MASTER_STATE.md`
4. This file

## Primary Command

Run the full refresh with:

```powershell
python scripts/management/refresh_all.py --own-account 62848015857
```

Machine-readable status is written to:

```text
reports/data/agent-refresh-status.json
```

If `ok` is `true`, open:

```text
reports/management-dashboard.html
```

If `ok` is `false`, inspect `steps[].stderr`, `payment_csv_validations[].errors`, and `missing_outputs`.

## Input Drop Contract

The agent may place files under `docs/_ai_context/inputs/`. Recommended folders:

| Channel | Folder | Examples |
|---|---|---|
| Email attachments | `docs/_ai_context/inputs/inbox/email/` | Supplier invoices, Nett Pay List, OFX exports, OCR text |
| OneDrive sync/export | `docs/_ai_context/inputs/inbox/onedrive/` | Schedule of Accounts workbook |
| Manual upload | `docs/_ai_context/inputs/inbox/manual/` | Bank statements, corrected spreadsheets |
| Dated batch | `docs/_ai_context/inputs/YYYYMMDD/` | Payroll/payment spec sample packs |

The ingest ledger derives `ingest_channel` from the path. No email, OneDrive, or OAuth credentials belong in this repository.

## Current Capabilities

| Capability | Status | Primary files |
|---|---|---|
| POS Day End / Month End parsing | Active | `scripts/management/parse_reports.py` |
| File ledger and report-type series | Active | `scripts/management/build_file_repo.py` |
| OCR synthesis text parsing | Active for `deepseek*.txt` style text | `scripts/management/parse_ocr_whatsapp.py` |
| Bank OFX parsing | Active | `scripts/management/parse_external_inputs.py` |
| Supplier schedule summary | Active, schedule workbook only | `scripts/management/parse_external_inputs.py` |
| Payroll Nett Pay List to FNB CSV | Active | `scripts/payroll/netpay_to_payment_csv.py` |
| FNB payment CSV validation | Active | `scripts/payroll/validate_payment_csv.py` |
| Dashboard refresh | Active | `scripts/management/generate_dashboard.py` |
| Agent orchestration | Active | `scripts/management/refresh_all.py` |

## Payroll Workflow

Input: `Nett Pay List*.xls*`

Rules:

- Employee codes are entity-neutral and match `^[A-Z]\d+`.
- Only `ACB` pay-method rows are included in FNB payment CSVs.
- `Cash` and other non-ACB rows are excluded from the payment CSV and recorded in the conversion metadata.
- Generated CSVs are validated for 36-column shape, payment date, nominated account, hash total, recipient fields, branch code, amount, and references.

Validated sample anchors:

| Source file | Included rows | Excluded rows | CSV total | Hash |
|---|---:|---:|---:|---|
| `Nett Pay List - 140526.xls` | 16 | 0 | R 32,095.27 | `062848016516` |
| `Nett Pay List - 210526.xlsx` | 16 | 0 | R 31,449.03 | `062848016516` |
| `Nett Pay List - 060526.xlsx` | 24 | 3 | R 56,575.22 | `062848016885` |

## AP / Invoice Workflow

Target business flow:

1. Operations creates an inventory order or request.
2. Supplier delivers stock.
3. Inventory is posted and becomes available for sale.
4. Supplier invoice arrives by email or manual upload.
5. Account schedule arrives from OneDrive, email, or manual upload.
6. Bank statement verifies payment.
7. Dashboard shows status and reconciliation evidence.

Implemented today:

- Schedule workbook summary via `supplier_schedule`.
- Bank OFX parsing via `bank_statement`.
- Creditors purchase files are classified as `creditors_purchases_detail`.
- Dashboard shows workflow readiness and explicitly marks invoice matching as pending until sample-backed parsing exists.

Do not mark supplier invoice matching as complete until real invoice and account schedule samples validate the parser.

## Safe Agent Behavior

- Never write secrets or credentials into the repo.
- Never import a payment CSV into banking automatically.
- Never modify `docs/_ai_context/knowledge/` without human approval.
- Use `reports/data/agent-refresh-status.json` as the control-plane response.
- If a file is classified as `unknown`, leave it in the ledger and request human review.
- If payment validation fails, stop and report the exact validator errors.

## Validation Commands

```powershell
python -m unittest tests.test_netpay_to_payment_csv
python scripts/management/refresh_all.py --own-account 62848015857
python scripts/payroll/validate_payment_csv.py reports/payroll/Payment_060526.csv --own-account 62848015857
```
