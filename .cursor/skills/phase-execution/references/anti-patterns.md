# Anti-Patterns

Patterns that cause phase execution to fail. Each includes the root cause and the correct alternative.

## Execution Anti-Patterns

| Anti-Pattern | Why It Fails | Instead |
|--------------|-------------|---------|
| Defer a P1 item without approval | P1 items were marked critical for a reason — deferring silently creates compounding debt | Ask the user before deferring any P1 item |
| Add config key without verifying code reads it | Config changes have zero runtime effect if no code consumes them | Trace: config file → loader function → consumer function |
| Mark phase complete while regressions exist | Future phases inherit broken state and attribute new bugs to their own changes | Fix the regression or document it with root cause before closing |
| Skip validation and declare "done" | Silent failures propagate downstream, causing much larger failures later | Run every validation command specified in the plan |
| Use `except: pass` on critical dependencies | Entire subsystem silently disabled — may go undetected for weeks | Log a warning or raise an error on critical paths |
| Use `except ImportError: pass` on load-bearing imports | Feature appears to work but produces empty/wrong output | Fail loudly: log what's missing and how to install it |

## Context Anti-Patterns

| Anti-Pattern | Why It Fails | Instead |
|--------------|-------------|---------|
| "Continue from where we left off" | New session has no memory of prior work | Reference specific file paths and state |
| "Use the data we extracted earlier" | Agent doesn't know what data or where it lives | Provide exact path + format + sample |
| "Same as before" | Ambiguous — "before" could be anything | Repeat the full specification |
| Loading entire large files | Blows the context window, degrades response quality | Read specific sections on demand |
| Implicit validation | Assumes things worked without checking | Explicit validation step with runnable command |
| Claiming checks passed without running them | False confidence — bug ships undetected | Execute the command, paste the output |

## Data Anti-Patterns

| Anti-Pattern | Why It Fails | Instead |
|--------------|-------------|---------|
| Using `encoding='utf-8'` for CSV files | BOM character corrupts first column header | Always use `utf-8-sig` |
| Assuming column names from documentation | Column names may have changed since docs were written | Read first 3 rows of the actual file |
| Accessing a field without verifying it exists | Returns None silently, produces wrong downstream results | Check schema documentation AND read a sample entry |
| Adding a scoring signal without selectivity evidence | Uniform boosts waste entire phases — they don't change relative ordering | Verify signal fires on true positives more than false positives |
| Silent fallback to default values | Bug hides behind a "reasonable" default | Log a warning when falling back, with what was expected vs. what happened |

## Planning Anti-Patterns

| Anti-Pattern | Why It Fails | Instead |
|--------------|-------------|---------|
| References "as discussed" | Next agent has zero conversation context | Include all context in the plan file |
| Numbers without sources | "Precision is 21%" — from when? which config? | "Precision: 21.9% (v5.10.0, report at path/to/report.json)" |
| Vague validation | "Verify it works" | Specific command: `python3 test.py --check metric >= 0.80` |
| Missing file inventory | Agent doesn't know what to read or create | List every file with path and action (READ/MODIFY/CREATE) |
