# JSON Schema Validation for Knowledge Files

## Overview

JSON Schema validates the structure of knowledge files before promotion. This prevents structural drift (missing required fields, wrong types, invalid enum values) that causes silent failures downstream.

Use JSON Schema [draft-07](https://json-schema.org/draft-07/json-schema-release-notes.html) or later.

## Common Patterns

### Glossary Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Glossary Schema",
  "type": "object",
  "required": ["version", "domain", "terms"],
  "properties": {
    "version": {"type": "string", "pattern": "^\\d+\\.\\d+\\.\\d+$"},
    "domain": {"type": "string", "minLength": 1},
    "terms": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": ["name", "definition"],
        "properties": {
          "name": {"type": "string", "minLength": 1},
          "definition": {"type": "string", "minLength": 10},
          "synonyms": {
            "type": "array",
            "items": {"type": "string"}
          },
          "domain": {"type": "string"},
          "source": {"type": "string"}
        }
      }
    }
  }
}
```

### Taxonomy Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Taxonomy Schema",
  "type": "object",
  "required": ["version", "categories"],
  "properties": {
    "version": {"type": "string"},
    "categories": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["name", "level"],
        "properties": {
          "name": {"type": "string"},
          "level": {"type": "integer", "minimum": 0},
          "parent": {"type": ["string", "null"]},
          "children": {
            "type": "array",
            "items": {"type": "string"}
          },
          "description": {"type": "string"}
        }
      }
    }
  }
}
```

### Enum Constraints

Use `enum` to restrict values to a known set:

```json
{
  "domain": {
    "type": "string",
    "enum": ["finance", "engineering", "operations", "analytics", "security"]
  },
  "authority_level": {
    "type": "string",
    "enum": ["high", "medium", "low"]
  }
}
```

### Pattern Matching

Use `pattern` for structured identifiers:

```json
{
  "api_id": {
    "type": "string",
    "pattern": "^API-[A-Z]{2,4}-\\d{3,5}$"
  },
  "version": {
    "type": "string",
    "pattern": "^\\d+\\.\\d+\\.\\d+$"
  }
}
```

## Creating Schemas for Your Domain

1. Start with one knowledge file (e.g., your glossary)
2. List all required fields and their types
3. Identify fields with constrained values (use `enum`)
4. Identify fields with structured formats (use `pattern`)
5. Write the schema and validate against your existing file
6. Iterate: add `minLength`, `minimum`, `minItems` constraints as needed

## Validation with Python

```python
import json
import yaml
import jsonschema

def validate_knowledge_file(data_path: str, schema_path: str) -> list[str]:
    """Validate a YAML knowledge file against a JSON Schema."""
    with open(schema_path, "r") as f:
        schema = json.load(f)

    with open(data_path, "r") as f:
        data = yaml.safe_load(f)

    validator = jsonschema.Draft7Validator(schema)
    errors = []
    for error in sorted(validator.iter_errors(data), key=lambda e: list(e.path)):
        path = ".".join(str(p) for p in error.path) or "(root)"
        errors.append(f"  {path}: {error.message}")

    return errors
```

## Best Practices

- One schema per knowledge file type (glossary, taxonomy, catalog)
- Store schemas in `knowledge/schemas/` alongside the knowledge files
- Run validation before every promotion (automated in staging workflow)
- Version your schemas alongside your knowledge files
- Use `additionalProperties: false` sparingly — it blocks extensibility
- Use `description` fields in schemas for documentation
