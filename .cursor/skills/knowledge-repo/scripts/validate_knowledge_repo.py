#!/usr/bin/env python3
"""
Knowledge Repository Validator

Validates the health of a knowledge repository by checking:
1. CURRENT_VERSION exists and matches a versions/ directory
2. All YAML files in reference/ parse without errors
3. All JSON Schema files in schemas/ are valid JSON Schema
4. CHANGELOG.md exists

Usage:
    python validate_knowledge_repo.py --knowledge-root docs/_ai_context/knowledge
    python validate_knowledge_repo.py --knowledge-root docs/_ai_context/knowledge --verbose
"""

import argparse
import json
import sys
from pathlib import Path

EXIT_OK = 0
EXIT_WARNINGS = 1
EXIT_ERRORS = 2


def check_current_version(root: Path, verbose: bool) -> list[str]:
    """Check CURRENT_VERSION file exists and points to a valid version snapshot."""
    errors = []
    version_file = root / "CURRENT_VERSION"

    if not version_file.exists():
        errors.append(f"MISSING: {version_file} — no version tracking")
        return errors

    version = version_file.read_text().strip()
    if not version:
        errors.append(f"EMPTY: {version_file} — version string is blank")
        return errors

    if verbose:
        print(f"  CURRENT_VERSION: {version}")

    versions_dir = root / "versions"
    if versions_dir.exists():
        expected_dir = versions_dir / f"v{version}"
        if not expected_dir.exists():
            alt_dir = versions_dir / version
            if not alt_dir.exists():
                errors.append(
                    f"MISMATCH: CURRENT_VERSION is '{version}' but neither "
                    f"versions/v{version}/ nor versions/{version}/ exists"
                )

    return errors


def check_yaml_files(root: Path, verbose: bool) -> tuple[list[str], list[str]]:
    """Check all YAML files in reference/ and domain/ parse without errors."""
    errors = []
    warnings = []

    try:
        import yaml
    except ImportError:
        warnings.append("SKIP: PyYAML not installed — cannot validate YAML files")
        return errors, warnings

    for subdir in ["reference", "domain", "glossary"]:
        dir_path = root / subdir
        if not dir_path.exists():
            continue

        yaml_files = list(dir_path.glob("*.yaml")) + list(dir_path.glob("*.yml"))
        if verbose:
            print(f"  Checking {len(yaml_files)} YAML files in {subdir}/")

        for yf in yaml_files:
            try:
                with open(yf, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                if data is None:
                    warnings.append(f"EMPTY: {yf.relative_to(root)} — file parses but contains no data")
                elif verbose:
                    print(f"    OK: {yf.name}")
            except yaml.YAMLError as e:
                errors.append(f"PARSE ERROR: {yf.relative_to(root)} — {e}")

    return errors, warnings


def check_json_schemas(root: Path, verbose: bool) -> tuple[list[str], list[str]]:
    """Check all JSON Schema files in schemas/ are valid JSON."""
    errors = []
    warnings = []

    schemas_dir = root / "schemas"
    if not schemas_dir.exists():
        warnings.append("SKIP: schemas/ directory does not exist")
        return errors, warnings

    json_files = list(schemas_dir.glob("*.json"))
    if verbose:
        print(f"  Checking {len(json_files)} JSON Schema files in schemas/")

    for jf in json_files:
        try:
            with open(jf, "r", encoding="utf-8") as f:
                schema = json.load(f)

            if "$schema" not in schema and "type" not in schema:
                warnings.append(
                    f"SUSPECT: {jf.relative_to(root)} — missing both '$schema' and 'type' "
                    f"fields (may not be a JSON Schema)"
                )
            elif verbose:
                print(f"    OK: {jf.name}")

        except json.JSONDecodeError as e:
            errors.append(f"PARSE ERROR: {jf.relative_to(root)} — {e}")

    return errors, warnings


def check_changelog(root: Path, verbose: bool) -> list[str]:
    """Check CHANGELOG.md exists."""
    warnings = []
    changelog = root / "CHANGELOG.md"
    if not changelog.exists():
        warnings.append(f"MISSING: {changelog.relative_to(root)} — no changelog file")
    elif verbose:
        print(f"  CHANGELOG.md exists ({changelog.stat().st_size} bytes)")
    return warnings


def check_governance(root: Path, verbose: bool) -> list[str]:
    """Check governance directory has essential files."""
    warnings = []
    gov_dir = root / "governance"
    if not gov_dir.exists():
        warnings.append("MISSING: governance/ directory — no governance structure")
        return warnings

    essential = ["GOVERNANCE_POLICY.md", "PENDING_UPDATES.yaml"]
    for fname in essential:
        fpath = gov_dir / fname
        if not fpath.exists():
            warnings.append(f"MISSING: governance/{fname}")
        elif verbose:
            print(f"  governance/{fname} exists")

    return warnings


def main():
    parser = argparse.ArgumentParser(description="Validate knowledge repository health")
    parser.add_argument(
        "--knowledge-root",
        type=str,
        default="docs/_ai_context/knowledge",
        help="Path to knowledge repository root",
    )
    parser.add_argument("--verbose", action="store_true", help="Print detailed output")
    args = parser.parse_args()

    root = Path(args.knowledge_root)
    if not root.exists():
        print(f"ERROR: Knowledge root does not exist: {root}")
        sys.exit(EXIT_ERRORS)

    print(f"Validating knowledge repository: {root.resolve()}")
    print()

    all_errors = []
    all_warnings = []

    print("[1/5] Checking CURRENT_VERSION...")
    all_errors.extend(check_current_version(root, args.verbose))

    print("[2/5] Checking YAML files...")
    yaml_errors, yaml_warnings = check_yaml_files(root, args.verbose)
    all_errors.extend(yaml_errors)
    all_warnings.extend(yaml_warnings)

    print("[3/5] Checking JSON Schemas...")
    schema_errors, schema_warnings = check_json_schemas(root, args.verbose)
    all_errors.extend(schema_errors)
    all_warnings.extend(schema_warnings)

    print("[4/5] Checking CHANGELOG.md...")
    all_warnings.extend(check_changelog(root, args.verbose))

    print("[5/5] Checking governance structure...")
    all_warnings.extend(check_governance(root, args.verbose))

    print()
    print("=" * 60)

    if all_errors:
        print(f"ERRORS ({len(all_errors)}):")
        for e in all_errors:
            print(f"  ✗ {e}")

    if all_warnings:
        print(f"WARNINGS ({len(all_warnings)}):")
        for w in all_warnings:
            print(f"  ⚠ {w}")

    if not all_errors and not all_warnings:
        print("ALL CHECKS PASSED — knowledge repository is healthy")
        sys.exit(EXIT_OK)
    elif all_errors:
        print(f"\nFAILED: {len(all_errors)} errors, {len(all_warnings)} warnings")
        sys.exit(EXIT_ERRORS)
    else:
        print(f"\nPASSED with {len(all_warnings)} warnings")
        sys.exit(EXIT_WARNINGS)


if __name__ == "__main__":
    main()
