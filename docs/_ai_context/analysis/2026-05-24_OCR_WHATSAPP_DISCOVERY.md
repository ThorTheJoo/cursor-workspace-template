---
document_type: ANALYSIS
status: ACTIVE
traceability_id: "OCR-WHATSAPP-2026-05-24"
---

# OCR WhatsApp Discovery — Multi-Source Reconciliation Phase

**Site:** ENGEN JET PARK SERVICE STATION  
**Input:** `deepseek_text_20260524_26b077.txt` — synthesized OCR from ~20 WhatsApp JPEG images  
**Channel:** WhatsApp → camera photos of POS/ATG/CIT screens → DeepSeek OCR → consolidated text

## Data Source Model (5 layers)

| Layer | Tag | Trust | Examples |
|-------|-----|-------|----------|
| POS System | `pos_system` | Authoritative daily ops | Day End `.TXT`, EFT batch |
| Bank Feed | `bank_feed` | Authoritative cash movement | FNB `.ofx` |
| Payroll | `payroll_system` | Authoritative wages | Nett Pay List |
| Manual Recon | `manual_recon` | Authoritative adjustments | Cash Up, Schedule of Accounts |
| OCR WhatsApp | `ocr_whatsapp` | Reference — confirm vs POS/bank | ATG photos, CIT receipts, EOD screenshots |

## OCR Extract Summary

| Section | Records | Key finding |
|---------|---------|-------------|
| ATG tank dips | 5 daily snapshots (20–24 May) | ULP95 below 5-day safety stock by 24 May |
| Fuel volume daily | 4 days (18–21 May) | 5,000.67 L on 20 May matches POS Batch 143 |
| Pump vs tank EOD | Batches 141, 144 | B144 −39.94 L → REVIEW |
| Shop daily | 4 days | 20 May Dry Stock R16,754.80 = POS shop incl |
| CIT pickups | 5 collections + 1 drop | Not equal to daily sales (expected) |
| Staff exceptions | SIA +R1,110.25 on 18 May | Investigate |
| Alerts | Delivery needed 16 May; low ULP95/diesel days | Reorder fuel |

## Cross-Source Reconciliations (validated)

| Check | Date | Source A | Source B | Result |
|-------|------|----------|----------|--------|
| Fuel volume | 2026-05-20 | OCR 5,000.67 L | POS B143 5,000.67 L | **MATCH** |
| Shop sales | 2026-05-20 | OCR Dry Stock R16,754.80 | POS Shop Incl R16,754.80 | **MATCH** |
| Pump vs tank | 2026-05-21 | OCR B144 pump 5,361 L | OCR ATG 5,401 L | **REVIEW** (−39.94 L) |
| Wet stock DSL | 2026-05-22 | POS pump 2,068 L | POS tank 2,047 L | **REVIEW** (+20.59 L) |
| EFT vs bank | — | POS daily batch | Bank Apr OFX | **PENDING** (period mismatch) |
| Payroll vs bank | — | 2 Nett Pay Lists | Bank debits | **PENDING** (await fresh bank) |

## Thresholds (from OCR extract)

- Reserve level: 1,000 L per grade
- Min days of stock: 5 days (reorder trigger)
- Pump vs tank variance: ±25 L per ~5,000 L day
- Cash variance: investigate if > R50

## Pipeline

```
deepseek_text_*.txt  →  parse_ocr_whatsapp.py  →  canonical.external.ocr_whatsapp
POS Day End *.TXT    →  parse_reports.py       →  canonical.daily / daily_history
                              ↓
                    build_reconciliations()  →  canonical.external.reconciliations
                              ↓
                    generate_dashboard.py    →  management-dashboard.html
```

## Next Steps (discovery phase)

1. **Bank refresh** — user to provide latest FNB transactions (same period as EFT batches)
2. **Invoices** — supplier invoice drops for creditor recon
3. **More Day End files** — extend daily_history for 18–21 May POS-side comparisons
4. **Deep-parse Cash Up** — tie CIT pickups to petty cash workbook
5. **OCR quality** — when Excel/PDF exports available, prefer over WhatsApp photos
