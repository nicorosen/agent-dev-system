#!/usr/bin/env python3
"""Render the provider-neutral scaffold into a staging directory.

This script never writes into a target repo directly. It renders templates into
an output directory so the result can be inspected before copying.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_ROOT = ROOT / "templates"


COPY_MAP = {
    "AGENTS.md": "AGENTS.md",
    "CLAUDE.md": "CLAUDE.md",
    "agent": ".agent",
    "codex": ".codex",
}

TOKEN_RE = re.compile(r"\{\{([A-Z0-9_]+)\}\}")


def template_files(include_provider_adapters: bool) -> list[Path]:
    files = [TEMPLATE_ROOT / "AGENTS.md"]
    files.extend(path for path in sorted((TEMPLATE_ROOT / "agent").rglob("*")) if path.is_file())
    if include_provider_adapters:
        files.append(TEMPLATE_ROOT / "CLAUDE.md")
        files.extend(path for path in sorted((TEMPLATE_ROOT / "codex").rglob("*")) if path.is_file())
    return files


def required_tokens(include_provider_adapters: bool) -> set[str]:
    tokens: set[str] = set()
    for path in template_files(include_provider_adapters):
        tokens.update(TOKEN_RE.findall(path.read_text(encoding="utf-8")))
    return tokens


def load_values(path: Path | None, include_provider_adapters: bool) -> dict[str, str]:
    loaded = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(loaded, dict):
        raise SystemExit("values file must be a JSON object")

    required = required_tokens(include_provider_adapters)
    provided = set(loaded)
    missing = sorted(required - provided)
    unknown = sorted(provided - required)

    errors = []
    if missing:
        errors.append("missing values: " + ", ".join(missing))
    if unknown:
        errors.append("unknown values: " + ", ".join(unknown))

    values: dict[str, str] = {}
    for key, value in loaded.items():
        if not isinstance(value, str):
            errors.append(f"value must be a string: {key}")
            continue
        if not value.strip():
            errors.append(f"value must not be blank: {key}")
            continue
        values[key] = value

    if errors:
        raise SystemExit("\n".join(errors))

    return values


def render_text(text: str, values: dict[str, str]) -> str:
    rendered = text
    for key, value in values.items():
        rendered = rendered.replace("{{" + key + "}}", value)
    return rendered


def render_file(src: Path, dst: Path, values: dict[str, str]) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    text = src.read_text(encoding="utf-8")
    dst.write_text(render_text(text, values), encoding="utf-8")
    dst.chmod(src.stat().st_mode & 0o777)


def render_tree(src: Path, dst: Path, values: dict[str, str]) -> None:
    for path in sorted(src.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(src)
        render_file(path, dst / rel, values)


def main() -> int:
    parser = argparse.ArgumentParser(description="Render scaffold templates into a staging directory.")
    parser.add_argument("--values", type=Path, required=True, help="JSON file with template values.")
    parser.add_argument("--out", type=Path, required=True, help="Output staging directory.")
    parser.add_argument(
        "--include-provider-adapters",
        action="store_true",
        help="Include CLAUDE.md and .codex adapter templates.",
    )
    parser.add_argument("--force", action="store_true", help="Replace the output directory if it exists.")
    args = parser.parse_args()

    out = args.out.resolve()
    if out.exists():
        if not args.force:
            raise SystemExit(f"output directory already exists: {out}")
        shutil.rmtree(out)
    out.mkdir(parents=True)

    values = load_values(args.values, args.include_provider_adapters)
    render_file(TEMPLATE_ROOT / "AGENTS.md", out / COPY_MAP["AGENTS.md"], values)
    render_tree(TEMPLATE_ROOT / "agent", out / COPY_MAP["agent"], values)

    if args.include_provider_adapters:
        render_file(TEMPLATE_ROOT / "CLAUDE.md", out / COPY_MAP["CLAUDE.md"], values)
        render_tree(TEMPLATE_ROOT / "codex", out / COPY_MAP["codex"], values)

    print(f"rendered scaffold: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
