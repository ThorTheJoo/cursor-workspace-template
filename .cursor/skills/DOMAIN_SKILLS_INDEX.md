---
document_type: STATE
status: ACTIVE
version: "1.0.0"
generated: "2026-05-24"
---

# Domain Skills Index

Retail, fuel, finance, and operations skills installed for **Experiment JP**.

## Custom (Fuel & C-Store)

| Skill | Purpose |
|-------|---------|
| `fuel-station-operations` | Forecourt ops, wet stock, shift reconciliation, UST compliance |
| `convenience-store-operations` | C-store inventory, foodservice, shrink, vendor orders, site P&L |
| `fuel-petrochemical-inventory` | Terminal/rack, BOL reconciliation, blending, bulk supply chain |

## Operations (agent-skills-ops)

| Skill | Source |
|-------|--------|
| `inventory-demand-planning` | [penglidu0623-dotcom/agent-skills](https://github.com/penglidu0623-dotcom/agent-skills) |
| `energy-procurement` | Same — energy/fuel cost & tariff optimization |
| `returns-reverse-logistics` | Same — retail returns & reverse logistics |

## Retail Inventory & Merchandising (writer/skills)

| Skill | Purpose |
|-------|---------|
| `inventory-risk-alerting` | Overstock/stockout severity alerts |
| `replenishment-recommendation` | Reorder quantity suggestions |
| `demand-forecast-explanation` | Forecast driver narratives |
| `shrinkage-risk-detector` | Theft/fraud pattern detection |
| `sell-through-velocity-tracker` | Velocity vs. benchmarks |
| `store-performance-narratives` | Store KPI storytelling |
| `sku-rationalization-advisor` | Assortment cleanup |
| `category-performance-diagnosis` | Category health analysis |
| `supplier-risk-monitor` | Supplier reliability risks |
| `competitive-price-monitoring` | Local price intelligence |

## Finance & P&L (writer/skills)

| Skill | Purpose |
|-------|---------|
| `margin-decomposition` | Margin driver breakdown |
| `cash-flow-variance-analysis` | Cash flow variance explanation |
| `revenue-leakage-detection` | Revenue leak identification |
| `cost-to-serve-decomposition` | Cost-to-serve analysis |
| `liquidity-forecast-narratives` | Liquidity position narratives |
| `branch-performance-analysis` | Multi-site/branch benchmarking |

## E-Commerce Retail Commands

| Skill | Commands |
|-------|----------|
| `ecommerce-retail` | `/inventory-forecast`, `/price-strategy`, `/customer-segment`, +7 more |

See `ecommerce-retail/commands/` for full command library.

## Source Cache

Cloned repos live in `.tools-cache/` (gitignored):

- `anthropics-skills` — official Anthropic skills
- `writer-skills` — 199 enterprise skills
- `agent-skills-ops` — logistics/retail/energy capabilities
- `r03-ecommerce-retail` — ecommerce command suite

## Refresh Skills

```powershell
# Re-clone and re-copy a source
git -C .tools-cache/writer-skills pull
Copy-Item -Path .tools-cache\writer-skills\skills\inventory-risk-alerting -Destination .cursor\skills\inventory-risk-alerting -Recurse -Force
```

Or re-run: `.\setup-tools.ps1 -Preset minimal`
