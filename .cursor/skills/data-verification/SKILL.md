---
name: data-verification
description: "Verify data file schemas, column headers, and field existence before writing any parsing code. Use whenever code reads CSV files, accesses JSON fields, consumes dataclass/dict structures, or a plan references fields on any data structure. Triggers on: CSV parsing, pandas read_csv, JSON field access, dataclass extension, DataFrame operations, schema validation, or any code that opens a data file."
metadata:
  author: mdd-framework
  version: "1.0.0"
  tier: portable
---

# Data Verification

The number one cause of data pipeline bugs is code that assumes field names without checking. A function reads `row["customer_id"]` but the CSV header is `CustomerID`. A script accesses `record.get("integration_apis")` but that field only exists on a different table. A dataclass gets extended with new fields that no consumer ever reads. These bugs are silent — they produce empty results instead of errors, and you lose hours tracing why the output is wrong.

This skill codifies a single principle: **never trust documentation about data shapes. Always verify from the actual file.**

Every minute spent verifying headers, field names, and data flows before writing code saves an hour of debugging silent failures after.

## Core Principle

Before writing any code that reads, transforms, or extends a data structure, physically read the actual data source and verify its shape matches your assumptions. Documentation drifts. Code comments lie. The file itself is the only truth.

## CSV Verification

Before writing any CSV parsing code, verify the actual file structure. Do not copy column names from documentation or prior code — read them from the file.

### Verification Steps

1. **Read the first 3 lines** of the actual CSV file to verify exact column headers
2. **Check for BOM** (Byte Order Mark): corporate tools like Excel prepend a BOM to UTF-8 files. Use `encoding='utf-8-sig'` for all CSV reading — it handles BOM transparently and works correctly on files without BOM
3. **Verify the delimiter** — do not assume comma. Check for tab, semicolon, or pipe separators
4. **After opening the file**, compare `reader.fieldnames` against expected headers. Log the mismatch and raise an error if they differ
5. **Check your schema registry** (if one exists) for the file's documented schema before reading

### Why `utf-8-sig`

The `utf-8-sig` codec strips the BOM on read and adds it on write. It is safe to use on files that do not have a BOM — it behaves identically to `utf-8` in that case. Using plain `utf-8` on a BOM file causes the first column header to include invisible characters, which silently breaks `row["column_name"]` lookups.

### Common Pitfalls

- Excel inserts line breaks *inside* quoted fields — `csv.reader` handles this but naive `line.split(",")` does not
- Trailing commas create a phantom empty column
- Numeric fields stored as strings with leading zeros (ZIP codes, IDs)

For detailed patterns and example code, see `references/csv-verification.md`.

## JSON and YAML Verification

Before writing code that accesses fields on a JSON or YAML data structure, read one sample entry from the actual file and confirm the field exists.

### Verification Steps

1. **Read one sample entry** from the actual JSON/YAML file
2. **Check your schema registry** for the structure's documented fields
3. **For nested fields**, verify each level of the path exists. `data["users"][0]["profile"]["email"]` has four levels — any could be `None` or missing
4. **Check the "does NOT have" list** — if your schema registry tracks which fields do *not* exist on a structure, consult it before assuming a field is present
5. **Never assume a field exists on one structure because a related structure has it.** Table A having `api_list` does not mean Table B also has it

### Common Pitfalls

- `None` vs missing key: `record.get("field")` returns `None` for both "field exists with value None" and "field does not exist"
- Empty arrays vs null: `[]` and `null` have different semantics in most code paths
- JSON field names are case-sensitive — `customerID` is not `customer_id`

For detailed patterns, see `references/json-verification.md`.

## Dataclass and Dict Extension

When you need to add fields to a data structure (dataclass, TypedDict, dict convention), you must trace the full data flow before making changes.

### Producer → Container → Consumer Audit

Every data field has three participants:

1. **Producer** — the function that creates or populates the field
2. **Container** — the class, dict, or structure that holds it
3. **Consumer** — the function(s) that read the field downstream

Before extending any container:

1. **Read the current definition** — see what fields already exist
2. **Add the new fields to the container FIRST** — before writing producer code
3. **Verify the consumer can access the new fields** — trace downstream code
4. **If adding optional fields**, ensure consumers handle `None` gracefully

### Why Order Matters

Adding a field to the producer without adding it to the container means the field is computed but never stored. Adding it to the container without updating the consumer means it is stored but never used. Both are waste. Trace the full chain before writing any code.

For the full audit methodology, see `references/producer-consumer-audit.md`.

## Silent Failure Prevention

Silent failures are the most expensive bugs in data pipelines. Code that swallows errors produces empty or partial results that look correct until someone notices missing data days later.

### Prohibited Patterns

| Pattern | Why It Fails | Replacement |
|---------|-------------|-------------|
| `except: pass` | Swallows all errors including critical ones | Catch specific exceptions, log WARNING |
| `except ImportError: pass` | Hides missing dependencies | Let it crash or log ERROR with install instructions |
| `row.get("col")` without None check | Returns None silently if column missing | Check result, raise if unexpected None |
| `return []` in error path | Caller sees empty list, not an error | Raise exception or log WARNING with context |
| `if not data: return` | Silently skips processing | Log what was expected and what was received |

### Required Patterns

- Every fallback path MUST log a WARNING with what was expected and what was received
- If a data lookup returns `None` for a field that should exist, RAISE an error — do not silently continue
- Every function that reads data must validate at least the first row or entry before processing the rest
- Use validation-first structure: validate inputs → process → validate outputs

For detailed examples and templates, see `references/silent-failure-prevention.md`.

## Quick Checklist

Use this table as a pre-flight check before writing data access code.

| If you are writing code that... | Verify first... |
|--------------------------------|-----------------|
| Reads a CSV file | Read first 3 lines, verify headers, use `utf-8-sig` |
| Accesses a JSON field | Read one sample entry, verify field exists |
| Accesses a nested field path | Verify each level exists, not just the leaf |
| Extends a dataclass or dict | Read current definition, trace Producer→Container→Consumer |
| Adds a new field to a producer | Verify the container has the field AND the consumer reads it |
| Uses `row.get()` or `dict.get()` | Check what happens when the value is `None` |
| Has a `try/except` around data access | Ensure the `except` block logs context, not just passes |
| Returns empty list or None on failure | Ensure the caller distinguishes "no results" from "error" |

## References

| File | Content |
|------|---------|
| `references/csv-verification.md` | Encoding patterns, delimiter detection, header validation, example code |
| `references/json-verification.md` | Sample reading, nested field access, schema registry patterns |
| `references/producer-consumer-audit.md` | Full Producer→Container→Consumer tracing methodology |
| `references/silent-failure-prevention.md` | Anti-patterns, required patterns, validation-first template |
