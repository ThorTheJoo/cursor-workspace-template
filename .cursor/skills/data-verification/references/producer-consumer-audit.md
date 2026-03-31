# Producer → Container → Consumer Audit

## Overview

Every data field in a pipeline flows through three stages:

1. **Producer** — a function that creates or populates the field value
2. **Container** — the class, dict, or data structure that holds the field
3. **Consumer** — one or more functions that read the field downstream

Bugs happen when these three stages are out of sync. This reference describes how to audit a data flow systematically.

## Audit Methodology

### Step 1: Identify the Field

Start with the field you are adding, modifying, or debugging. Write down:
- Field name (exact string key or attribute name)
- Data type (string, int, list, dict, optional)
- Expected value range (e.g., "always non-empty string" or "list of 0-N items")

### Step 2: Trace the Producer

Find every function that sets this field. Search for:
- Direct assignment: `container.field_name = value` or `container["field_name"] = value`
- Constructor: `MyDataclass(field_name=value)`
- Dict comprehension: `{"field_name": computed_value, ...}`

For each producer, verify:
- Is the field actually populated (not just defined)?
- What happens on error — does the producer set `None`, skip the field, or raise?
- Is the field set conditionally (only in some code paths)?

### Step 3: Verify the Container

Read the container definition (dataclass, TypedDict, or documented dict convention).

- Does the field exist in the definition?
- Is it typed correctly? (e.g., `Optional[str]` vs `str`)
- If the field is new, has the definition been updated BEFORE the producer writes to it?

### Step 4: Trace the Consumer

Find every function that reads this field. Search for:
- Attribute access: `container.field_name`
- Dict access: `container["field_name"]` or `container.get("field_name")`
- Destructuring: `field_name = container.field_name`

For each consumer, verify:
- Does the consumer handle `None` / missing values?
- Does the consumer expect a specific type?
- Will the consumer break if the producer is conditionally skipped?

## Example Audit

**Scenario:** Adding an `email_verified` field to a user record.

| Stage | Component | Verification |
|-------|-----------|-------------|
| Producer | `verify_email()` in `auth/verification.py` | Sets `user.email_verified = True` after email link clicked |
| Container | `UserProfile` dataclass in `models/user.py` | Must add `email_verified: bool = False` field |
| Consumer | `can_post()` in `permissions.py` | Checks `user.email_verified` before allowing posts |
| Consumer | `user_dashboard()` in `views/profile.py` | Displays verification badge |

**Audit findings:**
1. Container missing the field → add `email_verified: bool = False` to `UserProfile`
2. Producer only runs on email verification flow → `email_verified` defaults to `False` for existing users
3. Consumer `can_post()` handles the default correctly (unverified = cannot post)
4. Consumer `user_dashboard()` needs to handle `False` case (show "verify email" prompt)

## Dataclass Extension Protocol

When extending a dataclass with new fields:

1. **Add the field to the class definition first** — with a sensible default value
2. **Update the producer** — populate the new field in all code paths that create the object
3. **Update the consumer** — use the new field where needed
4. **Test the zero-value case** — ensure existing objects (created before your change) work with the default

```python
# STEP 1: Add field to container (with default)
@dataclass
class SearchResult:
    title: str
    score: float
    relevance_reason: str = ""  # NEW — added before producer/consumer

# STEP 2: Update producer
def search(query: str) -> list[SearchResult]:
    for hit in raw_results:
        yield SearchResult(
            title=hit["title"],
            score=hit["score"],
            relevance_reason=explain_score(hit),  # NEW — populate
        )

# STEP 3: Update consumer
def display_results(results: list[SearchResult]):
    for r in results:
        print(f"{r.title} ({r.score})")
        if r.relevance_reason:  # NEW — use with None-safe check
            print(f"  Reason: {r.relevance_reason}")
```

## Checklist

Before merging code that adds or modifies a data field:

- [ ] Field exists in the container definition (not just produced/consumed)
- [ ] Producer populates the field in ALL relevant code paths
- [ ] Consumer handles the default/None case
- [ ] If the field is optional, the consumer checks before accessing
- [ ] Existing data (created before this change) works with the default value
