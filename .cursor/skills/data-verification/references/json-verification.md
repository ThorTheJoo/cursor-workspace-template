# JSON and YAML Verification Reference

## Sample Entry Reading

Before writing field access code, always read at least one sample entry to confirm the structure.

```python
import json

with open(filepath, "r", encoding="utf-8") as f:
    data = json.load(f)

if isinstance(data, list) and data:
    sample = data[0]
    print(f"Sample keys: {list(sample.keys())}")
    print(f"Sample entry: {json.dumps(sample, indent=2)[:500]}")
elif isinstance(data, dict):
    if "entries" in data:
        sample = data["entries"][0] if data["entries"] else None
        print(f"Entry keys: {list(sample.keys()) if sample else 'EMPTY'}")
    else:
        print(f"Top-level keys: {list(data.keys())}")
```

## Nested Field Access Verification

Deep field paths are fragile. Verify each level before accessing.

### Unsafe Pattern

```python
# Crashes if any intermediate key is missing
email = data["users"][0]["profile"]["contact"]["email"]
```

### Safe Pattern

```python
def safe_get(obj, *keys, default=None):
    """Navigate nested dicts/lists safely."""
    for key in keys:
        if isinstance(obj, dict):
            obj = obj.get(key)
        elif isinstance(obj, (list, tuple)) and isinstance(key, int):
            obj = obj[key] if 0 <= key < len(obj) else None
        else:
            return default
        if obj is None:
            return default
    return obj

email = safe_get(data, "users", 0, "profile", "contact", "email")
```

## Schema Registry Lookup Pattern

If your project maintains a schema registry (e.g., a YAML file documenting data structures), consult it before writing access code.

```python
import yaml

def verify_field_exists(schema_path: str, structure_name: str, field_name: str) -> bool:
    with open(schema_path, "r") as f:
        schemas = yaml.safe_load(f)

    structure = schemas.get(structure_name, {})
    fields = structure.get("fields", {})
    does_not_have = structure.get("does_NOT_have", [])

    if field_name in does_not_have:
        raise ValueError(
            f"Field '{field_name}' is explicitly listed as NOT present "
            f"on '{structure_name}'. Check your data source."
        )

    return field_name in fields
```

## Common JSON/YAML Gotchas

| Issue | Symptom | Solution |
|-------|---------|----------|
| `None` vs missing key | `dict.get("x")` returns `None` for both | Use `"x" in dict` to distinguish |
| Empty array vs null | `[]` and `null` behave differently downstream | Check explicitly: `if data.get("items") is None` |
| Case sensitivity | `customerID` ≠ `customer_id` ≠ `CustomerId` | Normalize or verify exact casing from sample |
| YAML type coercion | `yes`/`no` become `True`/`False`, `1.0` becomes float | Use quotes in YAML: `"yes"`, `"1.0"` |
| Unicode in keys | Invisible characters in field names | Print `repr(key)` to inspect |
| Assuming related structures share fields | Table A has `api_list`, so Table B must too | Verify each structure independently |

## Verification Before Access

```python
import json
import logging

def load_and_verify(filepath: str, required_fields: set[str]) -> list[dict]:
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    entries = data if isinstance(data, list) else data.get("entries", [])

    if not entries:
        logging.warning(f"No entries in {filepath}")
        return []

    sample = entries[0]
    actual_fields = set(sample.keys())
    missing = required_fields - actual_fields
    if missing:
        raise ValueError(
            f"File {filepath} missing required fields: {missing}. "
            f"Available fields: {sorted(actual_fields)}"
        )

    return entries
```
