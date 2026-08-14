# misalud-lab-lis Agent-System Audit

Date: 2026-08-14
Target repo: `/Users/nicorosen/code_projects/misalud/misalud-lab-lis`
Mode: read-only audit

## Executive Summary

`misalud-lab-lis` is a high-safety, HIPAA-relevant local application with substantial Claude-specific agent infrastructure already in place. The migration should preserve the existing safety model and extract it into a provider-neutral `AGENTS.md` plus `.agent/` policy pack, while leaving Claude and Codex as thin adapters.

The repo is not ready for a broad mechanical rewrite. It has active uncommitted user work, live PHI/credential-sensitive local artifacts, advisory git hooks, and a paid Claude review gate. The first migration batch should only add neutral policy files and bounded read-only scripts, then update provider adapters in a second checkpoint.

## Current State

- Current branch: `A12-prd19-environment-column`.
- Uncommitted changes already exist in:
  - `installer/Uninstall-MiSaludStation.ps1`
  - `scripts/preflight_event.py`
  - `scripts/prod_test_patients.py`
  - `src/google_sheet_orders.py`
  - `src/order_store.py`
  - `src/station_workflow.py`
  - `src/xlsx_uploader.py`
  - `tests/test_order_store.py`
- Worktrees: only the main worktree was listed for this checkout.
- Branch inventory is large, with many task branches across PRD, security, fix, and feature tracks.
- No `AGENTS.md` found.
- No `.codex/` found.
- No `.agent/` found.
- `CLAUDE.md` exists and is concise but provider-specific.
- `.claude/agents/lead-engineer.md` is tracked.
- `.claude/commands/lead-review.md`, `.claude/settings.json`, `.claude/settings.local.json`, and `.claude/scheduled_tasks.lock` exist locally but are ignored by `.gitignore`.

## Existing Agent Rules

`CLAUDE.md` already contains important repo-local safety and cost controls:

- Default search scope should be `src/`, `tests/`, and `scripts/`.
- Do not read/search large or sensitive paths unless explicitly asked:
  - `dist/`
  - `context/`
  - `artifacts/`
  - `backup/`
  - `_ds/`
  - `__pycache__/`
  - `.venv/`
  - `*.db`
  - `orders.db.*`
  - `emulator_inbox.jsonl`
  - raw terminal/API scratch files
- Avoid dumping whole files, DB tables, or long logs.
- Suggest compaction around 40-50 tool calls or at task boundaries.
- The station can write to production paths and push real patient results to Crelio.
- Do not add blanket shell permissions.

These rules should move almost verbatim into neutral policy files and be referenced by provider adapters.

## Claude Configuration

Repo `.claude/settings.json` allows common git, search, Python syntax/test, and review-gate commands. It also allows `git reset *`, which should be reviewed before reusing in a provider-neutral policy because it is broad and potentially destructive.

Repo `.claude/settings.local.json` allows Crelio WebFetch and a commit-file variant. This is local and should not become canonical.

Global Claude settings include:

- model: `opus`
- effort level: `medium`
- global `Bash(ssh *)` permission
- `SessionEnd` hook invoking `~/.claude/hooks/sync_session_costs.py`

Global Claude instructions include Google Sheets MCP details and a service account workflow. That is useful context but should not be copied into this repo's canonical `AGENTS.md` unless a repo-specific task requires it.

## Codex Configuration

Codex config trusts `/Users/nicorosen/code_projects/misalud/misalud-lab-lis`.

Current Codex defaults:

- model: `gpt-5.5`
- reasoning effort: `medium`
- service tier: `priority`
- memories enabled
- plugin ecosystem enabled, including GitHub, Google Drive/Calendar, Slack, Supabase, Vercel, browser/chrome/computer-use, documents, spreadsheets, presentations, pdf, sites, and superpowers.

No repo `.codex/` adapter was found. The migration should add only repo-scoped Codex guidance, not duplicate global configuration.

## Review Hooks And Gates

Tracked hook infrastructure exists:

- `.githooks/lead_gate_common.sh`
- `.githooks/pre-commit`
- `.githooks/pre-merge-commit`
- `.githooks/pre-push`

Local git config:

- `core.hooksPath=.githooks`
- `lead-gate.advisory=true`

The lead gate is intentionally advisory by default and shells out to `scripts/lead_review.py`, which calls a Claude `lead-engineer` agent and writes artifacts under `artifacts/lead-review/`.

Important existing safeguards in `scripts/lead_review.py`:

- Excludes `dist/**`, `context/**`, `artifacts/**`, `backup/**`, `_ds/**`, `*.db`, `orders.db.*`, `emulator_inbox.jsonl`, `*.xlsx`, `.venv/**`, and `__pycache__/**`.
- Enforces max budget, file count, and diff-line constraints.
- Records `cost_usd` and `session_id` in review artifacts.
- Caches reviews by diff fingerprint.
- Re-derives verdicts from `docs/ARCHITECTURE_DOCTRINE.md` instead of trusting the model output.

This is a strong candidate to generalize into provider-neutral review policy while keeping Claude as the first concrete implementation.

## Security And HIPAA Policy Surface

The repo has mature safety documentation:

- `docs/ARCHITECTURE_DOCTRINE.md`
- `docs/SECURITY_REVIEW.md`
- `docs/SECURITY_DECISIONS.md`
- `docs/THREAT_MODEL.md`
- `docs/INCIDENT_RESPONSE.md`
- `docs/TESTING_GUIDE.md`
- `docs/EXECUTION_RUNBOOK.md`
- `docs/security-remediation/`

Key doctrine examples that must be preserved:

- No PHI in logs, exceptions, or status rendering.
- No credentials in tracked files or URL paths.
- No `.github/`, deploy key, CI runner, or new remote without satisfying the D-1 rotation trigger first.
- Patient-linked storage needs retention and pruning analysis.
- Config should resolve through `config_loader` rather than raw config access.

## Generated, Heavy, And Sensitive Paths

Observed heavy or sensitive local paths include:

- `backups/` about 732 MB
- `.git/` about 565 MB
- `dist/` about 189 MB
- `.venv/` about 127 MB
- `context/` about 73 MB
- `artifacts/` about 65 MB
- `logs/` about 49 MB
- `backup/` about 24 MB
- many `orders.db*` variants, including multiple full-PHI database copies
- `temp/`, `stationA/`, `stationB/`, root `station-config.json`, `.env`, `.env.enc`, `google_sheets_token.json`

`.gitignore` is detailed and security-aware. It records prior leakage modes and should be treated as a policy source, not just an ignore file.

## Scripts And Tests

The repo is Python-based, with:

- Main command: `python run.py`
- Test command: `python -m pytest tests/ -v`
- Syntax check: `python3 -m py_compile <files>`
- Many operational scripts under `scripts/`.
- Important safety scripts:
  - `scripts/lead_review.py`
  - `scripts/preflight_event.py`
  - `scripts/prod_test_patients.py`
  - `scripts/erase_patient.py`
  - `scripts/validate_station.py`
  - `scripts/install_hooks.sh`
- Important safety tests:
  - `tests/test_repository_hygiene.py`
  - `tests/test_log_redaction.py`
  - `tests/test_read_audit.py`
  - `tests/test_retention.py`
  - `tests/test_webhook_auth.py`

The first migration should not run full tests unless a repo change is approved. For documentation-only adapter work, verification can start with path checks, ignore checks, and targeted policy linting.

## Gaps Against Target Architecture

- Missing canonical provider-neutral `AGENTS.md`.
- Missing `.agent/` shared policy pack.
- Missing `.codex/` adapter.
- `CLAUDE.md` currently carries canonical repo instructions instead of importing a neutral source.
- Existing `.claude/agents/lead-engineer.md` is provider-specific and directly tied to Claude model naming.
- Existing telemetry is strong for `lead_review.py`, but not yet normalized across providers, sessions, tasks, and merged PRs.
- Existing worktree/task isolation exists by practice and branch naming, but not as a provider-neutral contract.
- No bounded, provider-neutral command wrappers yet for agent status/diff/test context.

## Risk Notes

- Do not touch the current branch without coordinating around existing uncommitted changes.
- Do not read or summarize patient data artifacts.
- Do not add CI, remotes, deploy keys, or GitHub automation without addressing `SECURITY_DECISIONS.md` D-1 first.
- Do not convert ignored local Claude settings into tracked policy.
- Do not weaken `.gitignore` exceptions.
- Review the existing `git reset *` Claude permission before translating it into any shared adapter.

## Recommendation

Proceed with a staged migration:

1. Add neutral policy files without changing behavior.
2. Add bounded helper scripts and telemetry schema.
3. Convert provider adapters to reference the neutral policy.
4. Generalize the review gate after the neutral policy proves stable in the pilot.

Stop before Phase 1 implementation and get explicit approval for the first file batch.

