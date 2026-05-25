---
name: fuel-petrochemical-inventory
description: >
  Fuel and petrochemical inventory management — terminal operations, product quality,
  blend specifications, BOL reconciliation, temperature/volume correction, pipeline/
  rack scheduling, and supply chain exception handling. Use for petroleum products,
  diesel, gasoline grades, ethanol blending, terminal lift, rack price, or bulk fuel
  inventory across depots and sites.
license: MIT
version: 1.0.0
metadata:
  domain: petrochemical-fuel
  tags: ["petroleum", "petrochemical", "terminal", "rack", "BOL", "blending"]
---

# Fuel & Petrochemical Inventory

## Role and Context

You manage bulk fuel inventory across terminals, depots, and downstream retail sites. You understand ASTM fuel specs, temperature/volume correction (API/NIST), ethanol/RFG blending rules, BOL reconciliation, and supply allocation during shortage or allocation events. You work with jobbers, majors, terminal operators, and carriers.

## When to Use

- Terminal lift scheduling and inventory allocation
- BOL vs. received volume reconciliation
- Product quality/spec deviation (octane, sulfur, water/sediment)
- Blend optimization (in RFG/subgrade markets)
- Rack price analysis and supply contract review
- Bulk tank farm inventory (depot level)
- Allocation/rationing during supply disruption
- Cross-dock and multi-leg delivery planning

## Core Knowledge

### Volume Correction

```
Corrected Volume = Observed Volume × CF(Temperature)
```

Track gross vs. net gallons. Delivery disputes often stem from temperature at load vs. unload.

### Product Grades & Blending

| Product | Key specs | Notes |
|---------|-----------|-------|
| Regular 87 | RVP season, octane | Ethanol blend wall |
| Midgrade 89 | Blend ratio | Often splash blend |
| Premium 93 | Octane target | Higher shrink sensitivity |
| Diesel ULSD | S15, lubricity, CFPP | Seasonal cold flow |
| DEF | ISO 22241 | Separate handling |

### BOL Reconciliation Workflow

1. Match BOL to delivery ticket and ATG receipt
2. Compare ordered vs. delivered vs. metered receipt
3. Investigate variance > 0.25% (temperature, line fill, theft, meter error)
4. Document with carrier/terminal if needed

### Supply Chain Exception Playbook

| Event | Actions |
|-------|---------|
| Terminal outage | Reroute lifts, extend site run-out horizon |
| Allocation | Prioritize high-volume/profitable sites |
| Price spike | Review hedging, retail pass-through timing |
| Quality fail | Quarantine tank, notify supplier, test retain |
| Carrier delay | Adjust order lead time, customer comms |

## Required Inputs

| Input | Description |
|-------|-------------|
| `terminal_inventory` | Tank levels at rack/terminal |
| `bol_records` | Bill of lading details |
| `site_demand_forecast` | Pull by site/grade |
| `contract_terms` | Lift rights, fees, allocation |
| `quality_tests` | Lab certs if quality issue |

## Output Specification

1. **Inventory position** by location and grade
2. **Lift schedule** with volumes and carriers
3. **Variance analysis** for any delivery mismatch
4. **Risk flags** — run-out dates, spec issues, allocation
5. **Financial impact** — rack margin, shrink cost, dispute exposure

## Related Skills

- `fuel-station-operations` — site-level wet stock
- `energy-procurement` — energy/fuel cost optimization
- `inventory-demand-planning` — demand forecasting
- `supplier-risk-monitor` — carrier/supplier reliability
