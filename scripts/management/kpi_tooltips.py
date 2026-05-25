#!/usr/bin/env python3
"""Plain-language KPI tooltip definitions for the management dashboard."""

from __future__ import annotations

KPI_TOOLTIPS: dict[str, str] = {
    "nett_takings": (
        "Daily Nett Takings answers: 'How much money should we have collected today?' "
        "We read the POS Day End Summary report, section 'Daily Takings Summary', line 'Nett Takings'. "
        "The POS adds up: Sales (fuel + shop) + Returns (refunds, shown negative) + Receipts (other money in) "
        "+ Payouts (money paid out to suppliers, shown negative). Example: if sales were R184,000 and payouts "
        "were R665, nett takings ≈ R183,805. This is the figure cashiers and card batches must reconcile to "
        "before banking."
    ),
    "fuel_sales": (
        "Fuel Sales is the rand value of all petrol and diesel sold on the forecourt for the day. "
        "Source: Day End Summary → EOD Summary by Category → FUEL row → Total Sales column. "
        "Litres shown are total pump volume (all grades). GP% is gross profit as a percentage "
        "of fuel sales — how much margin remains after fuel cost of sales."
    ),
    "shop_sales": (
        "Shop Sales is convenience-store turnover including VAT (inside sales only, not fuel). "
        "Source: Day End Summary category subtotal before the FUEL line. GP% shows how much "
        "profit the shop made after product cost — higher is better for categories like "
        "tobacco and beverages."
    ),
    "cash_variance": (
        "Cash Variance is the difference between cash actually counted (Actual) and what the "
        "POS expected (Theoretical) at day end. Source: Day End Summary → Cash Variance section, "
        "bottom total Variance column. Positive = over (extra cash). Negative = short. "
        "Industry target: investigate if over R50 or 0.25% of takings."
    ),
    "fuel_customers": (
        "Number of fuel customers is how many separate fuel transactions occurred — one customer "
        "may have multiple line items if they bought different grades. Source: Day End Summary "
        "statistics block. Useful for tracking footfall on the forecourt."
    ),
    "shop_customers": (
        "Number of shop customers is distinct convenience-store transactions (not fuel-only). "
        "Source: Day End Summary statistics. Compare with fuel customers to understand "
        "how many drivers also come inside the store."
    ),
    "eft_batch": (
        "EFT Batch total is card payments processed and batched for the bank on the batch date. "
        "Source: EFT Batch Summary By EFT Batch Date — Forecourt + Retail + General totals. "
        "This should eventually match what lands in the bank statement (minus fees and timing)."
    ),
    "eft_pending": (
        "EFT Pending are card transactions from the last shift that have not yet been sent to "
        "the bank. Source: EFT Transactions Not Yet Sent to Bank. These will appear in a "
        "future batch — normal to see a small amount right after day end."
    ),
    "stock_take": (
        "Stock Take variance counts SKUs where physical count differed from the system. "
        "Source: Stock Take Variance report. 'Variance @ cost' is the rand value of "
        "over/under stock at last cost — shrink or counting errors to investigate."
    ),
    "wet_stock": (
        "Wet Stock EOD compares fuel sold according to pump meters vs tank dipping (ATG). "
        "Source: Day End Summary → Fuel Sales Control EOD Short. Variance in litres: "
        "positive = pumps recorded more than tanks lost (possible meter issue or delivery timing); "
        "negative = tanks lost more than pumps show (possible leak, theft, or calibration)."
    ),
    "top_categories": (
        "Top shop categories ranked by sales value for the day. Source: Day End Summary "
        "EOD Summary by Category. GP% = (Sales − Cost of Sales) ÷ Sales × 100. "
        "Helps identify which departments drive turnover and margin."
    ),
    "mtd_fuel_variance": (
        "Month-to-date fuel variance % shows cumulative pump-vs-tank difference for each grade "
        "since month start. Source: Day End Summary → Fuel Sales Control MTD Summary. "
        "Target typically under 0.5%. High diesel variance may indicate delivery or temperature issues."
    ),
    "cashiers": (
        "Cashier EOS (End of Shift) exceptions show each operator's takings, void count and void "
        "value for the day. Source: Day End Summary → EOS Exceptions. High voids may indicate "
        "training issues, errors, or fraud risk worth reviewing."
    ),
    "monthly_reference": (
        "Monthly reference figures come from the Month End Summary report (not the daily file). "
        "Nett Takings = full month cash + cards + accounts. Banking variance = difference between "
        "cash counted and POS theoretical for the whole month."
    ),
    "daily_timeline": (
        "Daily Operations Timeline tells the story day by day in chronological order (oldest at top). "
        "Each row is one trading day. Δ (delta) columns show how much changed vs the previous day — "
        "green = up, red = down. The highlighted 'Latest' row matches the KPI snapshot cards below. "
        "CIT pickup comes from OCR WhatsApp photos; other columns from POS Day End when available."
    ),
    "daily_history": (
        "Daily history plots nett takings and cash variance for each Day End batch file found "
        "in your inputs folder. Drop new Day End Summary exports to extend this trend."
    ),
    "payroll": (
        "Payroll shows wages due to staff from the Nett Pay List — an export from your payroll "
        "provider (not the POS). We sum column 'Nett Pay' for all rows to get Total Net Pay. "
        "Each employee row is also converted to FNB Payment CSV format (BinSol v1.00): account "
        "number, branch code, amount, and references. The hash total on row 3 is calculated from "
        "all recipient account digits plus your nominated debit account — FNB uses this to verify "
        "the file was not altered. Import via FNB Online Banking → Payments → Import."
    ),
    "bank_statement": (
        "Bank statement figures come from an OFX file downloaded from FNB Online Banking — this "
        "is the actual record of money moving in and out of account 62848015857. Credits In = "
        "all positive amounts (deposits, card settlements). Debits Out = all negative amounts "
        "(payments, fees, payroll). Transaction count = number of lines on the statement. "
        "In future recons: match POS EFT batch totals to credit lines, and payroll CSV totals "
        "to debit lines around pay dates."
    ),
    "supplier_schedule": (
        "Schedule of Accounts is a manual Excel log of supplier invoices (GRVs) by department. "
        "Source: site management (manual recon). Total incl VAT helps track creditor spend "
        "outside the POS — reconcile against payouts and bank debits."
    ),
    "cash_up": (
        "Cash Up workbook is a manual month-end reconciliation tool maintained by site management "
        "(not exported from the POS). It typically includes petty cash counts, float movements, "
        "and expenses paid from the till that the forecourt system does not capture. "
        "Use it alongside the Month End Summary to explain differences between POS theoretical "
        "cash and what was actually banked."
    ),
    "input_registry": (
        "This table lists every data file found in your inputs folder and how we classify it. "
        "Blue = POS system (auto-generated daily exports). Pink = payroll (Nett Pay Lists). "
        "Green = bank feed (OFX downloads). Amber = manual recon (Excel workbooks you maintain). "
        "Purple = OCR WhatsApp (photos of reports, extracted via OCR). "
        "Source type tells future reconciliation workflows which file to trust for each question."
    ),
    "source_legend": (
        "Every figure on this dashboard is tagged by where it came from. POS (blue) = forecourt system "
        "export, highest trust for daily sales. Bank (green) = actual money movement. Payroll (pink) = "
        "wages file. Manual recon (amber) = Excel you maintain. OCR WhatsApp (purple) = photos forwarded "
        "on WhatsApp, OCR-extracted — useful but should be confirmed against POS or bank when possible."
    ),
    "atg_tank_levels": (
        "ATG (Automatic Tank Gauge) readings show how much fuel is physically in each underground tank, "
        "photographed from the tank monitoring screen and OCR'd from WhatsApp. We subtract a 1,000 L "
        "reserve (minimum safety stock) to get 'available' litres. Days-of-stock = available ÷ average "
        "daily sales. Below 5 days triggers a reorder alert. Compare with POS wet-stock variance to "
        "catch dip errors or delivery timing issues."
    ),
    "ocr_fuel_trend": (
        "Daily fuel volume by grade from OCR'd POS reports (WhatsApp photos). These litres should match "
        "the POS Day End export for the same date when we have both. Use this to spot trends (e.g. diesel "
        "spikes) before month-end. Pump-vs-tank variance rows compare what pumps recorded vs what the "
        "tank lost — target within ±25 L per ~5,000 L sold."
    ),
    "cit_pickups": (
        "CIT (Cash-In-Transit) bag removals are when the security company collects cash from site. "
        "Source: photos of CIT collection receipts via WhatsApp/OCR. The amount is NOT total daily "
        "sales — most turnover is cards/EFT. A R37,900 pickup on a R175,000 sales day is normal if "
        "only part of the cash is collected or multiple days accumulated. Reconcile against POS cash "
        "banking and manual Cash Up workbook."
    ),
    "reconciliation_matrix": (
        "This table shows what we compared against what, and the result. 'Match' = sources agree. "
        "'Review' = variance exceeds threshold — investigate. 'Pending' = we need more data (e.g. bank "
        "statement for the same day as EFT batch). 'Info' = explanatory comparison, not an error. "
        "Each row names Source A and Source B so you can see exactly where both numbers came from."
    ),
    "file_repository": (
        "File Repository lists each REPORT TYPE (not every duplicate filename). "
        "Series points = unique business periods we have extracted (e.g. one row per Day End batch). "
        "Full specification: file-type-catalog.yaml. History JSON: reports/data/series/. "
        "When you receive a new file, run build_file_repo.py then refresh the dashboard."
    ),
    "operational_alerts": (
        "Alerts from OCR extracts and threshold rules: low days-of-stock (reorder fuel), delivery-needed "
        "alarms from ATG, cashier till variances. These are early warning flags — confirm against "
        "the live system before acting."
    ),
}


SOURCE_LABELS = {
    "pos_system": "POS System",
    "payroll_system": "Payroll",
    "bank_feed": "Bank Feed",
    "manual_recon": "Manual Recon",
    "ocr_whatsapp": "OCR / WhatsApp",
    "inventory": "Inventory",
    "accounting": "Accounting",
}


def src_badge(source_type: str) -> str:
    label = SOURCE_LABELS.get(source_type, source_type.replace("_", " ").title())
    return f'<span class="tag tag-{source_type}">{label}</span>'


def tip_html(key: str) -> str:
    text = KPI_TOOLTIPS.get(key, "No description available.")
    return (
        f'<span class="tip" tabindex="0" aria-label="Help">'
        f'<span class="tip-icon">?</span>'
        f'<span class="tip-body">{text}</span>'
        f"</span>"
    )
