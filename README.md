# Agent Development System

Provider-neutral development-system templates, policies, and rollout plans for local repositories.

## Purpose

This project is the control plane for moving repo-specific agent instructions out of single-provider files and into reusable, provider-neutral policy packs.

Design work happens here. Target repos stay untouched until an explicit scaffold test or rollout step copies this structure into that repo.

The first pilot target is:

- `/Users/nicorosen/code_projects/misalud/misalud-lab-lis`

## Target Architecture

- Canonical `AGENTS.md` per repo.
- Minimal provider adapters: `CLAUDE.md`, `.claude/`, `.codex/`.
- Shared `.agent/` policies, task packets, scripts, and telemetry schema.
- One task per branch or worktree, with bounded agent-facing commands.
- Explicit exclusions for generated, large, credential-bearing, and PHI-sensitive paths.
- Reusable review, security, database, and documentation skills.
- Telemetry for cache misses/writes, total tokens, sessions per task, and cost per merged PR where available.

## Current Status

- Pilot audit completed read-only on 2026-08-14.
- No changes have been made to the pilot repo.
- Reusable scaffold templates are maintained inside this global project.
- First target-repo copy requires a separate approval and should happen only when testing the scaffold.

## Usage

Render a scaffold into a staging directory:

```bash
python3 scripts/render_scaffold.py \
  --values examples/misalud-lab-lis.values.json \
  --out /tmp/misalud-lab-lis-scaffold \
  --include-provider-adapters \
  --force
```

Check a rendered scaffold:

```bash
python3 scripts/check_scaffold.py /tmp/misalud-lab-lis-scaffold
```

Do not copy rendered files into a target repo until the scaffold-test checklist is approved.

## Key Files

- `templates/`: reusable provider-neutral scaffold.
- `scripts/render_scaffold.py`: renders templates into a staging directory only.
- `scripts/check_scaffold.py`: validates required files and references.
- `schemas/scaffold-values.schema.json`: required values contract for scaffold rendering.
- `schemas/agent-telemetry.schema.json`: sanitized telemetry record schema.
- `docs/scaffold-test-checklist.md`: target-repo copy and validation checklist.
- `docs/rollout-checklist.md`: repo-by-repo rollout process.
- `docs/phase-tracker.md`: persistent project todo list.
