# Pre-Flight Checklist

Run through this checklist before executing any phase.

## Phase Start Checklist

- [ ] Read the complete plan file before starting any work
- [ ] Read BACKLOG.md — list all items tagged `assigned: {this_phase}`
- [ ] Announce P1 items to the user before proceeding
- [ ] Verify all files listed in `depends_on` exist at stated paths
- [ ] Run pre-flight validation command if one is specified in the plan
- [ ] Check for aged backlog items (P1 items open > 2 phases → escalate)

## Wiring Verification

Before making any config or code change, trace the full wiring:

### Config Changes
- [ ] Config key is defined in the config file
- [ ] Config file is loaded by the application (find the loader code)
- [ ] The specific key is read by the consuming function (find the line)
- [ ] Default value is reasonable if key is missing

### Feature Flags
- [ ] Flag is defined in config
- [ ] Flag is checked in the code path it's supposed to control
- [ ] Both on and off paths are tested
- [ ] Flag default (on/off) is documented

### Data File References
- [ ] YAML file exists at the stated path
- [ ] YAML file is loaded at runtime (find the loader)
- [ ] Fields accessed in code match fields in the YAML file

### Index/Data Field References
- [ ] Field exists in the data structure (check the schema)
- [ ] Field is populated (not always empty/null)
- [ ] Code that reads the field handles the case where it's missing

### CSV Parsing
- [ ] Read first 3 rows to verify actual column headers
- [ ] Use `encoding='utf-8-sig'` (handles BOM from Excel)
- [ ] Verify delimiter matches expectations (comma, tab, semicolon)
- [ ] After reading, validate fieldnames match expectations — log and fail on mismatch

### JSON Field Access
- [ ] Read one sample entry to verify the field exists
- [ ] Check the schema documentation for the data structure
- [ ] Handle missing fields explicitly (don't silently return None)

### Dataclass Extensions
- [ ] Read the dataclass definition to see current fields
- [ ] If adding new fields: add to the dataclass FIRST
- [ ] Verify consumer code can access the new fields
- [ ] Trace: Producer → Container → Consumer

## Report Disconnects Before Making Changes

If any wiring check reveals a disconnect (e.g., config key not read by code, field doesn't exist in data), report the disconnect before making the change. This prevents investing time in changes that would have no runtime effect.
