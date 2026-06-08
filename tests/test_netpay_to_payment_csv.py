from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "payroll"))

from netpay_to_payment_csv import convert, find_payroll_files
from validate_payment_csv import validate_payment_csv


class NetPayToPaymentCsvTests(unittest.TestCase):
    def setUp(self) -> None:
        self.config = ROOT / "config" / "site.yaml"
        self.inputs = ROOT / "docs" / "_ai_context" / "inputs"

    def convert_to_temp(self, source: Path) -> dict:
        self.assertTrue(source.exists(), f"Missing fixture: {source}")
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        output = Path(temp_dir.name) / f"Payment_{source.stem}.csv"
        result = convert(source, output, self.config)
        validation = validate_payment_csv(output, "62848015857")
        self.assertTrue(validation["valid"], validation["errors"])
        self.assertEqual(validation["recipient_count"], result["employee_count"])
        self.assertEqual(validation["total_amount"], result["total_net_pay"])
        return result

    def test_find_payroll_files_is_recursive(self) -> None:
        files = [path.name for path in find_payroll_files(self.inputs)]
        self.assertIn("Nett Pay List - 140526.xls", files)
        self.assertIn("Nett Pay List - 210526.xlsx", files)
        self.assertIn("Nett Pay List - 060526.xlsx", files)

    def test_existing_140526_payroll_anchor(self) -> None:
        result = self.convert_to_temp(self.inputs / "Starter Docs" / "Nett Pay List - 140526.xls")
        self.assertEqual(result["employee_count"], 16)
        self.assertEqual(result["total_net_pay"], 32095.27)
        self.assertEqual(result["hash_total"], "062848016516")
        self.assertEqual(result["excluded_employee_count"], 0)

    def test_existing_210526_payroll_anchor(self) -> None:
        result = self.convert_to_temp(self.inputs / "Starter Docs" / "Nett Pay List - 210526.xlsx")
        self.assertEqual(result["employee_count"], 16)
        self.assertEqual(result["total_net_pay"], 31449.03)
        self.assertEqual(result["hash_total"], "062848016516")
        self.assertEqual(result["excluded_employee_count"], 0)

    def test_new_060526_payroll_excludes_cash_rows(self) -> None:
        result = self.convert_to_temp(self.inputs / "08062026" / "Nett Pay List - 060526.xlsx")
        self.assertEqual(result["source_employee_count"], 27)
        self.assertEqual(result["employee_count"], 24)
        self.assertEqual(result["excluded_employee_count"], 3)
        self.assertEqual(result["total_net_pay"], 56575.22)
        self.assertEqual(result["source_total_net_pay"], 62703.70)
        self.assertEqual(result["excluded_total_net_pay"], 6128.48)


if __name__ == "__main__":
    unittest.main()
