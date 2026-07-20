#!/usr/bin/env node
/**
 * Verifies every path listed in MASTER_STATE.md § Script Registry exists on disk.
 * Run from repo root: node scripts/verify_script_registry.js
 *
 * Expects a markdown section "## Script Registry" with backtick paths like
 * `scripts/foo.py` or `scripts/bar.js`.
 */
const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname, "..");
const masterPath = path.join(root, "docs", "_ai_context", "state", "MASTER_STATE.md");

if (!fs.existsSync(masterPath)) {
  console.error("FAIL: MASTER_STATE.md not found at", masterPath);
  process.exit(1);
}

const text = fs.readFileSync(masterPath, "utf8");
const start = text.indexOf("## Script Registry");
if (start === -1) {
  console.error("FAIL: No '## Script Registry' section in MASTER_STATE.md");
  process.exit(1);
}
const end = text.indexOf("\n## ", start + 5);
const section = end === -1 ? text.slice(start) : text.slice(start, end);

const paths = new Set();
const backtick = /\`(scripts\/[^`]+\.(?:py|js|sh|ps1)|bin\/[^`]+)\`/g;
let m;
while ((m = backtick.exec(section)) !== null) {
  paths.add(m[1]);
}

if (paths.size === 0) {
  console.log(
    "Script Registry verification SKIP: no script paths found under ## Script Registry"
  );
  process.exit(0);
}

const missing = [];
for (const rel of paths) {
  const full = path.join(root, rel);
  if (!fs.existsSync(full)) missing.push(rel);
}

if (missing.length) {
  console.error("Script Registry verification FAILED. Missing:");
  missing.forEach((p) => console.error("  -", p));
  process.exit(1);
}
console.log("Script Registry verification OK:", paths.size, "paths checked");
