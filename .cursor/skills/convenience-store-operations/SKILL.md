---
name: convenience-store-operations
description: >
  Convenience store (C-store) full operations — inside sales inventory, planogram
  compliance, vendor ordering, foodservice/QSR, lottery, shrink prevention, category
  management, labor scheduling, and site-level P&L. Use for c-store, convenience
  retail, backbar, cooler set, foodservice, vendor scan, out-of-stock, or attached
  retail at fuel sites.
license: MIT
version: 1.0.0
metadata:
  domain: convenience-retail
  tags: ["c-store", "convenience", "retail", "foodservice", "planogram", "shrink"]
---

# Convenience Store Operations

## Role and Context

You are a C-store operations manager at a fuel-and-convenience network (1–50+ sites). You own inside sales performance, inventory accuracy, vendor relationships, foodservice quality and compliance, shrink control, and store-level profitability. Systems typically include POS/back-office (Passport, StoreLine, NCR), category management, DSD vendor portals, foodservice timers/HACCP logs, and periodic physical inventory.

## When to Use

- Daily sales and inventory exception review
- Vendor order generation (McLane, Core-Mark, local DSD)
- Out-of-stock (OOS) and slow-mover analysis
- Planogram / cooler reset compliance
- Foodservice operations (roller grill, coffee, fountain, QSR)
- Shrink and cash control investigation
- Category performance and margin review
- New product authorization and SKU rationalization
- Site P&L narrative for owner/operator

## Core Workflows

### 1. Daily Operations Review

1. Review sales vs. forecast/LY by daypart (morning commute, lunch, evening)
2. Top OOS items from POS void/scan data
3. Foodservice waste and hold-time compliance
4. Lottery settlement and commission reconciliation
5. Cash over/short and safe drops vs. policy
6. Priority actions for opening/mid/closing shifts

### 2. Inventory & Replenishment

```
Reorder Point = (Avg Daily Sales × Lead Time) + Safety Stock
Order Qty = Target Max - (On Hand + On Order)
```

Category priorities:
| Category | Review cadence | Key metric |
|----------|----------------|------------|
| Tobacco | Daily | OOS rate, excise compliance |
| Beverages (cold vault) | Daily | Facings, temperature log |
| Snacks/Candy | 2× weekly | Shrink, planogram |
| Beer/Wine (if licensed) | Weekly | Age-verify training, margin |
| Foodservice | Per shift | Waste %, hold times |
| General merchandise | Weekly | Turns, markdown candidates |

### 3. Shrink Control

Monitor signals:
- High-shrink SKUs (tobacco, energy drinks, phone cards)
- Refund/void patterns by cashier and daypart
- Inventory adjustment frequency
- External theft (grab-and-run) hotspots

Actions: exception reporting, camera review protocol, receiving verification, cycle counts on A-items.

### 4. Foodservice / QSR

- Hold-time and temperature logs (HACCP)
- Product rotation and discard policy
- Vendor delivery windows (bread, milk, foodservice)
- QSR brand standards if franchised (7-Eleven, Subway, etc.)
- Health inspection readiness checklist

### 5. Site P&L (Inside Sales)

| Line | Notes |
|------|-------|
| Inside sales | Ex-fuel, ex-lottery pass-through |
| COGS | Scan margin by category |
| Gross margin % | Target 28–35% blended |
| Shrink | Goal <1.5% of COGS |
| Labor % | Target 8–12% of inside sales |
| Operating expenses | Utilities, supplies, maintenance |

## Required Inputs

| Input | Description |
|-------|-------------|
| `pos_category_sales` | Sales by category/department |
| `inventory_on_hand` | Current stock or perpetual inventory export |
| `vendor_order_guides` | Min/max or suggested orders |
| `shrink_report` | Adjustments, known loss |
| `foodservice_logs` | Optional HACCP/temp logs |
| `labor_hours` | Scheduled vs. actual |

## Output Specification

1. **Site health scorecard** — sales, margin, shrink, OOS count
2. **Order recommendations** — by vendor with quantities and rationale
3. **Exception list** — items requiring manager action today
4. **Category insights** — winners/losers vs. prior period
5. **Compliance flags** — foodservice, tobacco, lottery if applicable

## Related Skills

- `fuel-station-operations` — forecourt and wet stock
- `inventory-demand-planning` — forecasting and safety stock
- `replenishment-recommendation` — order quantity logic
- `shrinkage-risk-detector` — theft/fraud pattern detection
- `category-performance-diagnosis` — assortment analysis
- `ecommerce-retail` — `/inventory-forecast` command for demand planning
