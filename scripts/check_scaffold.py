#!/usr/bin/env python3
"""Check a rendered or copied scaffold for required files and references."""

from __future__ import annotations

import argparse
from pathlib import Path


REQUIRED_FILES = [
    "AGENTS.md",
    ".agent/README.md",
    ".agent/bin/agent_diff",
    ".agent/bin/agent_policy_check",
    ".agent/bin/agent_status",
    ".agent/bin/agent_test",
    ".agent/policies/repo-safety.md",
    ".agent/policies/context-budget.md",
    ".agent/policies/testing.md",
    ".agent/policies/review-gate.md",
    ".agent/policies/task-isolation.md",
    ".agent/task-packet-template.md",
]

TEMPLATE_FILES = [
    "AGENTS.md",
    "agent/README.md",
    "agent/bin/agent_diff",
    "agent/bin/agent_policy_check",
    "agent/bin/agent_status",
    "agent/bin/agent_test",
    "agent/policies/repo-safety.md",
    "agent/policies/context-budget.md",
    "agent/policies/testing.md",
    "agent/policies/review-gate.md",
    "agent/policies/task-isolation.md",
    "agent/task-packet-template.md",
]

REQUIRED_REFERENCES = [
    ".agent/policies/repo-safety.md",
    ".agent/policies/context-budget.md",
    ".agent/policies/testing.md",
    ".agent/policies/review-gate.md",
    ".agent/policies/task-isolation.md",
]

UNRESOLVED_MARKERS = ["{{", "}}"]


def main() -> int:
    parser = argparse.ArgumentParser(description="Check scaffold files and references.")
    parser.add_argument("path", type=Path, help="Rendered scaffold or target repo path.")
    parser.add_argument(
        "--allow-template-markers",
        action="store_true",
        help="Allow unresolved {{TOKEN}} markers. Use only for raw templates.",
    )
    parser.add_argument(
        "--template-root",
        action="store_true",
        help="Check raw templates where agent/ renders to .agent/.",
    )
    args = parser.parse_args()

    root = args.path.resolve()
    errors: list[str] = []
    required_files = TEMPLATE_FILES if args.template_root else REQUIRED_FILES

    for rel in required_files:
        path = root / rel
        if not path.is_file():
            errors.append(f"missing required file: {rel}")

    agents = root / "AGENTS.md"
    if agents.is_file():
        text = agents.read_text(encoding="utf-8")
        for ref in REQUIRED_REFERENCES:
            if ref not in text:
                errors.append(f"AGENTS.md missing reference: {ref}")

    if not args.allow_template_markers:
        for rel in required_files:
            path = root / rel
            if not path.is_file():
                continue
            text = path.read_text(encoding="utf-8")
            if any(marker in text for marker in UNRESOLVED_MARKERS):
                errors.append(f"unresolved template marker in: {rel}")

    if errors:
        for error in errors:
            print(f"FAIL {error}")
        return 1

    print(f"PASS scaffold valid: {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
