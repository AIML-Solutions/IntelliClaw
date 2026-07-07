from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class FixtureDemoTest(unittest.TestCase):
    def test_fixture_demo_generates_expected_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            result = subprocess.run(
                [sys.executable, "scripts/run_fixture_demo.py", "--out", str(out)],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertIn("[fixture-demo] wrote", result.stdout)

            raw = json.loads((out / "raw-claims.json").read_text(encoding="utf-8"))
            crosscheck = json.loads((out / "crosscheck-report.json").read_text(encoding="utf-8"))
            scored = json.loads((out / "scored-claims.json").read_text(encoding="utf-8"))
            minutes = (out / "running-minutes.md").read_text(encoding="utf-8")

            self.assertEqual(len(raw), 5)
            self.assertEqual(crosscheck["claims_reviewed"], 5)
            self.assertGreaterEqual(len(crosscheck["contradictions"]), 1)
            self.assertTrue(any(claim["risk"] == "high" for claim in scored))
            self.assertIn("Offline fixture demo only", minutes)


if __name__ == "__main__":
    unittest.main()
