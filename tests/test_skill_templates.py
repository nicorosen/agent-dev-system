from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = ROOT / "templates" / "skills"

EXPECTED_POLICY_REFERENCES = {
    "review.md": [
        "AGENTS.md",
        ".agent/policies/review-gate.md",
        ".agent/policies/context-budget.md",
        ".agent/policies/testing.md",
    ],
    "security.md": [
        "AGENTS.md",
        ".agent/policies/repo-safety.md",
        ".agent/policies/review-gate.md",
        ".agent/policies/context-budget.md",
    ],
    "database.md": [
        "AGENTS.md",
        ".agent/policies/repo-safety.md",
        ".agent/policies/testing.md",
        ".agent/policies/context-budget.md",
    ],
    "docs.md": [
        "AGENTS.md",
        ".agent/policies/repo-safety.md",
        ".agent/policies/task-isolation.md",
        ".agent/policies/context-budget.md",
    ],
}


class SkillTemplateTests(unittest.TestCase):
    def test_each_skill_cites_canonical_policies(self) -> None:
        for filename, references in EXPECTED_POLICY_REFERENCES.items():
            with self.subTest(filename=filename):
                text = (SKILL_DIR / filename).read_text(encoding="utf-8")
                for reference in references:
                    self.assertIn(reference, text)

    def test_each_skill_has_provider_adapter_guidance(self) -> None:
        for path in sorted(SKILL_DIR.glob("*.md")):
            with self.subTest(filename=path.name):
                text = path.read_text(encoding="utf-8")
                self.assertIn("## Provider Adapter Guidance", text)
                self.assertIn("Do not duplicate canonical policy", text)
                self.assertIn("provider-specific", text)


if __name__ == "__main__":
    unittest.main()
