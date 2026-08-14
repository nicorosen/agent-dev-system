from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
RENDER = ROOT / "scripts" / "render_scaffold.py"
CHECK = ROOT / "scripts" / "check_scaffold.py"
VALUES = ROOT / "examples" / "misalud-lab-lis.values.json"
FIXTURE_FILE_LIST = ROOT / "docs" / "fixtures" / "misalud-lab-lis-scaffold-file-list.txt"


class ScaffoldScriptTests(unittest.TestCase):
    def run_cmd(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, *args],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_templates_validate_with_markers_allowed(self) -> None:
        result = self.run_cmd(str(CHECK), "templates", "--template-root", "--allow-template-markers")
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("PASS scaffold valid", result.stdout)

    def test_rendered_scaffold_validates_without_markers(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "scaffold"
            render = self.run_cmd(
                str(RENDER),
                "--values",
                str(VALUES),
                "--out",
                str(out),
                "--include-provider-adapters",
            )
            self.assertEqual(render.returncode, 0, render.stderr + render.stdout)

            check = self.run_cmd(str(CHECK), str(out))
            self.assertEqual(check.returncode, 0, check.stderr + check.stdout)
            self.assertIn("PASS scaffold valid", check.stdout)
            self.assertTrue((out / "AGENTS.md").is_file())
            self.assertTrue((out / ".agent" / "README.md").is_file())
            self.assertTrue((out / "CLAUDE.md").is_file())
            self.assertTrue((out / ".codex" / "README.md").is_file())

            expected = sorted(
                line.strip()
                for line in FIXTURE_FILE_LIST.read_text(encoding="utf-8").splitlines()
                if line.strip()
            )
            actual = sorted(
                str(path.relative_to(out))
                for path in out.rglob("*")
                if path.is_file()
            )
            self.assertEqual(actual, expected)

    def test_agent_diff_reports_names_without_file_contents(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            out = tmp_path / "scaffold"
            render = self.run_cmd(
                str(RENDER),
                "--values",
                str(VALUES),
                "--out",
                str(out),
            )
            self.assertEqual(render.returncode, 0, render.stderr + render.stdout)

            repo = tmp_path / "repo"
            repo.mkdir()
            subprocess.run(["git", "init"], cwd=repo, capture_output=True, text=True, check=True)
            subprocess.run(
                ["git", "config", "user.email", "agent@example.invalid"],
                cwd=repo,
                capture_output=True,
                text=True,
                check=True,
            )
            subprocess.run(
                ["git", "config", "user.name", "Agent Test"],
                cwd=repo,
                capture_output=True,
                text=True,
                check=True,
            )
            tracked = repo / "tracked.txt"
            tracked.write_text("before\n", encoding="utf-8")
            subprocess.run(["git", "add", "tracked.txt"], cwd=repo, capture_output=True, text=True, check=True)
            subprocess.run(
                ["git", "commit", "-m", "seed"],
                cwd=repo,
                capture_output=True,
                text=True,
                check=True,
            )

            tracked.write_text("SECRET_PAYLOAD_SHOULD_NOT_PRINT\n", encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(out / ".agent" / "bin" / "agent_diff")],
                cwd=repo,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            self.assertIn("M\ttracked.txt", result.stdout)
            self.assertNotIn("SECRET_PAYLOAD_SHOULD_NOT_PRINT", result.stdout)

    def test_render_rejects_unknown_values(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            values = tmp_path / "values.json"
            values.write_text('{"UNKNOWN": "value"}', encoding="utf-8")
            result = self.run_cmd(str(RENDER), "--values", str(values), "--out", str(tmp_path / "out"))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("unknown values", result.stderr + result.stdout)


if __name__ == "__main__":
    unittest.main()
