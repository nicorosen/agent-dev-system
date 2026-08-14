from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
VALIDATE = ROOT / "scripts" / "validate_telemetry.py"
FIXTURES = ROOT / "examples" / "telemetry"


class TelemetryTests(unittest.TestCase):
    def run_cmd(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, *args],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_fixture_examples_validate_and_report_aggregates(self) -> None:
        result = self.run_cmd(str(VALIDATE), str(FIXTURES))
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("PASS telemetry valid: 2 record(s)", result.stdout)
        self.assertIn("task phase-6-fixture: sessions=2 total_cost=0.0175 cache_hit_ratio=0.2500", result.stdout)
        self.assertIn("merged_pr 1: sessions=2 total_cost=0.0175", result.stdout)

    def test_sensitive_raw_fields_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            record = Path(tmp) / "bad.json"
            record.write_text(
                """{
  "schema_version": "1.0",
  "repo": {"name": "example"},
  "task_id": "bad",
  "provider": "openai",
  "started_at": "2026-08-14T12:00:00Z",
  "prompt": "raw prompt must not be stored"
}
""",
                encoding="utf-8",
            )
            result = self.run_cmd(str(VALIDATE), str(record))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("forbidden telemetry field: prompt", result.stdout)


if __name__ == "__main__":
    unittest.main()
