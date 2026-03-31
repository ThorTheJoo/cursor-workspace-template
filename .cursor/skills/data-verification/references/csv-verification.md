# CSV Verification Reference

## Encoding Patterns

### Always Use `utf-8-sig`

```python
import csv

with open(filepath, "r", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    # utf-8-sig strips BOM if present, works normally if absent
```

### BOM Detection (for diagnostics)

```python
def has_bom(filepath: str) -> bool:
    with open(filepath, "rb") as f:
        return f.read(3) == b'\xef\xbb\xbf'
```

## Delimiter Detection

```python
import csv

def detect_delimiter(filepath: str) -> str:
    with open(filepath, "r", encoding="utf-8-sig") as f:
        sample = f.read(4096)
    sniffer = csv.Sniffer()
    dialect = sniffer.sniff(sample)
    return dialect.delimiter
```

## Header Validation

After opening a CSV file, compare actual headers against expected headers before processing any rows.

```python
import csv
import logging

EXPECTED_HEADERS = {"id", "name", "email", "department"}

with open(filepath, "r", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    actual = set(reader.fieldnames or [])

    missing = EXPECTED_HEADERS - actual
    if missing:
        raise ValueError(
            f"CSV {filepath} missing expected columns: {missing}. "
            f"Actual columns: {reader.fieldnames}"
        )

    extra = actual - EXPECTED_HEADERS
    if extra:
        logging.warning(f"CSV {filepath} has unexpected columns: {extra}")

    for row in reader:
        # Safe to proceed — headers verified
        process(row)
```

## Common CSV Gotchas

| Issue | Symptom | Solution |
|-------|---------|----------|
| BOM in header | First column key starts with `\ufeff` | Use `encoding='utf-8-sig'` |
| Embedded newlines | Row count seems wrong, fields split mid-value | Use `csv.reader` (handles RFC 4180 quoting) |
| Trailing commas | Extra empty-string column at end of every row | Strip or filter empty column |
| Mixed line endings | `\r\n` and `\n` in same file | Open with `newline=''` (Python csv module docs) |
| Numeric strings | ZIP code `00123` becomes `123` if parsed as int | Keep as string, convert only when needed |
| Quoted fields with commas | `"Smith, John"` split into two columns | Use `csv.reader`, never `line.split(",")` |

## Quick Validation Template

```python
import csv
import logging

def read_validated_csv(filepath: str, expected_cols: set[str]) -> list[dict]:
    with open(filepath, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)

        actual = set(reader.fieldnames or [])
        missing = expected_cols - actual
        if missing:
            raise ValueError(f"Missing columns in {filepath}: {missing}")

        rows = list(reader)
        if not rows:
            logging.warning(f"CSV {filepath} has headers but zero data rows")
        else:
            logging.info(f"CSV {filepath}: {len(rows)} rows, columns: {reader.fieldnames}")

        return rows
```
