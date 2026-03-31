# Silent Failure Prevention Reference

## Anti-Patterns

These patterns cause silent failures — bugs that produce wrong results without any visible error.

### 1. Bare Exception Swallowing

```python
# BAD: Swallows ALL errors including KeyboardInterrupt
try:
    result = process(data)
except:
    pass

# BAD: Hides missing dependencies — code silently skips functionality
try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False
    pass  # No logging, no warning — caller has no idea
```

### 2. Silent Empty Returns

```python
# BAD: Caller cannot distinguish "no results" from "error"
def find_records(query: str) -> list[dict]:
    try:
        return database.search(query)
    except ConnectionError:
        return []  # Looks like "no matches" to caller

# BAD: Silently produces partial data
def extract_fields(row: dict) -> dict:
    return {
        "name": row.get("name"),       # None if missing
        "email": row.get("email"),     # None if missing
        "score": row.get("score"),     # None if missing — but caller does math on it
    }
```

### 3. Unchecked Optional Access

```python
# BAD: row.get() returns None if column missing — no error raised
for row in csv_reader:
    customer_id = row.get("customer_id")
    # If column is "CustomerID" (case mismatch), customer_id is None
    # Code continues silently with None values
    process(customer_id)
```

## Required Patterns

### 1. Catch Specific Exceptions, Log Context

```python
import logging

try:
    result = process(data)
except ValueError as e:
    logging.warning(
        f"Failed to process record {data.get('id', 'unknown')}: {e}. "
        f"Expected format: dict with 'name' and 'value' keys. "
        f"Received keys: {list(data.keys()) if isinstance(data, dict) else type(data)}"
    )
    raise
```

### 2. Raise on Unexpected None

```python
def get_required_field(record: dict, field: str) -> str:
    value = record.get(field)
    if value is None:
        raise ValueError(
            f"Required field '{field}' is missing or None. "
            f"Available fields: {sorted(record.keys())}"
        )
    return value
```

### 3. Validate First Row Before Processing

```python
import csv
import logging

def process_csv(filepath: str, required_cols: set[str]):
    with open(filepath, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)

        actual_cols = set(reader.fieldnames or [])
        missing = required_cols - actual_cols
        if missing:
            raise ValueError(f"Missing columns: {missing}")

        rows = list(reader)
        if not rows:
            logging.warning(f"File {filepath} has headers but no data rows")
            return []

        first = rows[0]
        for col in required_cols:
            if first.get(col) is None:
                logging.warning(f"First row has None for required column '{col}'")

        return rows
```

### 4. Log Fallback Paths

```python
import logging

def resolve_entity(name: str) -> str:
    canonical = registry.get(name)
    if canonical:
        return canonical

    fuzzy = registry.fuzzy_match(name, threshold=0.8)
    if fuzzy:
        logging.info(f"Fuzzy matched '{name}' -> '{fuzzy}' (no exact match)")
        return fuzzy

    logging.warning(
        f"Could not resolve entity '{name}'. "
        f"No exact or fuzzy match in registry ({len(registry)} entries). "
        f"Returning original name unchanged."
    )
    return name
```

## Validation-First Template

Structure data processing functions to validate before processing.

```python
import logging

def transform_records(records: list[dict], config: dict) -> list[dict]:
    # 1. Validate inputs
    if not records:
        raise ValueError("Empty input: expected at least one record")

    required_fields = {"id", "name", "category"}
    sample = records[0]
    missing = required_fields - set(sample.keys())
    if missing:
        raise ValueError(f"Records missing required fields: {missing}")

    threshold = config.get("min_score")
    if threshold is None:
        raise ValueError("Config missing 'min_score' — verify config file is loaded")

    # 2. Process
    results = []
    skipped = 0
    for record in records:
        score = compute_score(record)
        if score < threshold:
            skipped += 1
            continue
        results.append({**record, "score": score})

    # 3. Validate outputs
    if not results and skipped == len(records):
        logging.warning(
            f"All {len(records)} records fell below threshold {threshold}. "
            f"Check if threshold is too high or data is unexpected."
        )

    logging.info(f"Transformed {len(results)}/{len(records)} records (skipped {skipped})")
    return results
```

## Checklist

Before committing code that handles data:

- [ ] No bare `except: pass` or `except ImportError: pass` on load-bearing dependencies
- [ ] Every fallback path logs a WARNING with expected vs actual
- [ ] `dict.get()` results are checked for None when the field is required
- [ ] Empty returns ([], None, "") are distinguishable from error returns
- [ ] First entry/row is validated before processing the full dataset
- [ ] Error messages include enough context to diagnose (file path, field name, available keys)
