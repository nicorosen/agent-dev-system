#!/usr/bin/env python3
"""Validate sanitized agent telemetry records and print aggregate metrics."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT / "schemas" / "agent-telemetry.schema.json"
FORBIDDEN_FIELDS = {
    "prompt",
    "prompts",
    "response",
    "responses",
    "raw_diff",
    "diff",
    "patch",
    "log_excerpt",
    "stack_trace",
    "database_rows",
    "phi",
    "credential",
    "credentials",
    "secret",
    "secrets",
    "customer_data",
}


def load_schema() -> dict[str, Any]:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def record_paths(path: Path) -> list[Path]:
    if path.is_dir():
        return sorted(path.rglob("*.json"))
    return [path]


def load_record(path: Path) -> dict[str, Any]:
    try:
        record = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"{path}: invalid JSON: {exc}") from exc
    if not isinstance(record, dict):
        raise ValueError(f"{path}: telemetry record must be a JSON object")
    return record


def find_forbidden_fields(value: Any, prefix: str = "") -> list[str]:
    found: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            field_path = f"{prefix}.{key}" if prefix else key
            if key in FORBIDDEN_FIELDS:
                found.append(field_path)
            found.extend(find_forbidden_fields(child, field_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            found.extend(find_forbidden_fields(child, f"{prefix}[{index}]"))
    return found


def validate_datetime(value: Any, field: str) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        return f"{field} must be a string or null"
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return f"{field} must be an ISO 8601 datetime"
    return None


def validate_record(path: Path, record: dict[str, Any], schema: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required = schema["required"]
    allowed = set(schema["properties"])

    for field in required:
        if field not in record:
            errors.append(f"{path}: missing required field: {field}")
    for field in record:
        if field not in allowed:
            errors.append(f"{path}: unknown field: {field}")

    for field in find_forbidden_fields(record):
        errors.append(f"{path}: forbidden telemetry field: {field}")

    if record.get("schema_version") != "1.0":
        errors.append(f"{path}: schema_version must be 1.0")

    if not isinstance(record.get("repo"), dict) or not record.get("repo", {}).get("name"):
        errors.append(f"{path}: repo.name is required")

    provider = record.get("provider")
    provider_enum = schema["properties"]["provider"]["enum"]
    if provider not in provider_enum:
        errors.append(f"{path}: provider must be one of: {', '.join(provider_enum)}")

    for field in ("started_at", "ended_at"):
        if field in record:
            error = validate_datetime(record[field], field)
            if error:
                errors.append(f"{path}: {error}")

    usage = record.get("usage", {})
    if usage is not None and not isinstance(usage, dict):
        errors.append(f"{path}: usage must be an object")
    if isinstance(usage, dict):
        for field, value in usage.items():
            if value is not None and (not isinstance(value, int) or value < 0):
                errors.append(f"{path}: usage.{field} must be a non-negative integer or null")

    cost = record.get("cost", {})
    if cost is not None and not isinstance(cost, dict):
        errors.append(f"{path}: cost must be an object")
    if isinstance(cost, dict):
        for field in ("total_cost", "review_cost"):
            value = cost.get(field)
            if value is not None and (not isinstance(value, int | float) or value < 0):
                errors.append(f"{path}: cost.{field} must be a non-negative number or null")

    artifacts = record.get("artifacts", [])
    if artifacts is not None and not isinstance(artifacts, list):
        errors.append(f"{path}: artifacts must be an array")
    if isinstance(artifacts, list):
        for index, artifact in enumerate(artifacts):
            if not isinstance(artifact, dict):
                errors.append(f"{path}: artifacts[{index}] must be an object")
                continue
            if artifact.get("sanitized") is not True:
                errors.append(f"{path}: artifacts[{index}].sanitized must be true")

    return errors


def ratio(numerator: int | None, denominator: int | None) -> float | None:
    if numerator is None or denominator in (None, 0):
        return None
    return numerator / denominator


def add_usage(target: dict[str, int | None], usage: dict[str, Any]) -> None:
    for field in ("input_tokens", "cache_read_tokens", "cache_write_tokens"):
        value = usage.get(field)
        if value is None:
            continue
        target[field] = (target.get(field) or 0) + value


def aggregate(records: list[dict[str, Any]]) -> list[str]:
    by_task: dict[str, dict[str, Any]] = defaultdict(
        lambda: {
            "sessions": 0,
            "total_cost": 0.0,
            "input_tokens": None,
            "cache_read_tokens": None,
            "cache_write_tokens": None,
        }
    )
    by_pr: dict[str, dict[str, Any]] = defaultdict(lambda: {"sessions": 0, "total_cost": 0.0})

    for record in records:
        task = by_task[record["task_id"]]
        task["sessions"] += 1
        task["total_cost"] += (record.get("cost") or {}).get("total_cost") or 0.0
        add_usage(task, record.get("usage") or {})

        merged_pr = record.get("merged_pr")
        if isinstance(merged_pr, dict):
            pr = by_pr[merged_pr["id"]]
            pr["sessions"] += 1
            pr["total_cost"] += (record.get("cost") or {}).get("total_cost") or 0.0

    lines: list[str] = []
    for task_id in sorted(by_task):
        task = by_task[task_id]
        hit_ratio = ratio(task["cache_read_tokens"], task["input_tokens"])
        hit_text = "null" if hit_ratio is None else f"{hit_ratio:.4f}"
        lines.append(
            f"task {task_id}: sessions={task['sessions']} "
            f"total_cost={task['total_cost']:.4f} cache_hit_ratio={hit_text}"
        )

    for pr_id in sorted(by_pr):
        pr = by_pr[pr_id]
        lines.append(f"merged_pr {pr_id}: sessions={pr['sessions']} total_cost={pr['total_cost']:.4f}")

    return lines


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate sanitized agent telemetry records.")
    parser.add_argument("path", type=Path, help="Telemetry JSON file or directory.")
    args = parser.parse_args()

    schema = load_schema()
    paths = record_paths(args.path)
    if not paths:
        print(f"FAIL no telemetry JSON files found: {args.path}")
        return 1

    records: list[dict[str, Any]] = []
    errors: list[str] = []
    for path in paths:
        try:
            record = load_record(path)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        errors.extend(validate_record(path, record, schema))
        records.append(record)

    if errors:
        for error in errors:
            print(f"FAIL {error}")
        return 1

    print(f"PASS telemetry valid: {len(records)} record(s)")
    for line in aggregate(records):
        print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
