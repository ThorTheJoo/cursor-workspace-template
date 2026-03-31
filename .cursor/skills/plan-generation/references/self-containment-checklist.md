# Self-Containment Checklist

Use this checklist to verify a plan can be executed by an agent with zero prior context.

## Context Independence

- [ ] Plan does not reference "as discussed earlier" or "from our conversation"
- [ ] Plan does not say "same as before" or "like we did previously"
- [ ] All numbers and metrics include their source (not "the current precision" but "precision: 21.9% from v5.10.0 regression report at path/to/report.json")
- [ ] Environment variables are listed with setup commands
- [ ] Python/system path configuration is documented
- [ ] All file paths are absolute or relative to a clearly stated root

## Executability

- [ ] Every step has a concrete command or code change (not "update the config")
- [ ] Code snippets include exact file paths and line numbers
- [ ] Before/after code is shown for modifications
- [ ] Validation command follows every significant step
- [ ] Dependencies (packages, tools, services) are listed with install commands

## Data Verification

Before writing code that reads data files, verify:

- [ ] CSV files: actual column headers match what the plan references (read first 3 rows)
- [ ] CSV encoding: always use `utf-8-sig` (corporate Excel files include BOM)
- [ ] JSON fields: sample entry confirms the field exists
- [ ] Data structures: verify against schema documentation
- [ ] If a field is claimed to exist on a data structure, confirm it's actually populated (not always empty)

## Producer→Container→Consumer Audit

For every new data field the plan introduces:

- [ ] **Producer**: which function creates/populates the field?
- [ ] **Container**: which class, dict, or data structure holds it?
- [ ] **Consumer**: which downstream function reads it?
- [ ] All three are consistent (same field name, same type, same semantics)

## Silent Failure Prevention

- [ ] No `except: pass` or `except ImportError: pass` on critical dependencies
- [ ] Every fallback path logs a warning with what was expected and what happened
- [ ] If a lookup returns None for an expected field, the code raises an error — not silently continues
- [ ] Every function that reads data validates at least the first row/entry before proceeding

## What Makes a Plan FAIL Self-Containment

| Pattern | Example | Fix |
|---------|---------|-----|
| Implicit context | "Fix the scoring as we discussed" | Include exact file, line, before/after code |
| Missing env setup | "Run the pipeline" | Include PYTHONPATH, env vars, venv activation |
| Unverified data refs | "Read the `status` column from the CSV" | Read actual CSV headers first |
| No validation | "Update the config and proceed" | Add: verify config loaded with `grep` or test command |
| Vague scope | "Improve performance" | Specify: "reduce query time from 4.2s to <2s by adding index on `user_id`" |
