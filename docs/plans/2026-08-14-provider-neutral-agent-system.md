# Provider-Neutral Agent Development System Plan

> For agentic workers: this plan is staged. Do not modify a target repo until the user approves the exact file batch for that phase.

**Goal:** Build a provider-neutral development system that preserves repo safety policies while letting Claude, Codex, and later providers consume the same canonical instructions.

**Architecture:** Keep this global control project as the source for templates, rollout checklists, and audits. Design and scaffold work happens here first. A target repo receives a canonical `AGENTS.md`, a shared `.agent/` policy pack, and minimal provider adapters only during an approved scaffold test or rollout.

**Pilot:** `/Users/nicorosen/code_projects/misalud/misalud-lab-lis`

## Phase 0: Control Project And Read-Only Pilot Audit

Status: complete.

Created in this control project:

- `README.md`
- `docs/audits/2026-08-14-misalud-lab-lis.md`
- `docs/plans/2026-08-14-provider-neutral-agent-system.md`

Pilot repo changes: none.

Checkpoint:

- User approves moving to Phase 1.

## Phase 1: Build Neutral Scaffold In Global Project

Purpose: create reusable provider-neutral templates without touching any target repo.

Proposed global files to create:

- `templates/AGENTS.md`
  - Canonical provider-neutral entrypoint template.
  - Imports or points to `.agent/policies/*.md`.
  - Carries placeholders for repo layout, exclusion list, safety, commands, and session hygiene.
- `templates/agent/README.md`
  - Explains policy pack layout and provider adapter contract.
- `templates/agent/policies/repo-safety.md`
  - PHI, credentials, external writes, production DB, hardware, Crelio, Google Sheets, and generated-file rules.
- `templates/agent/policies/context-budget.md`
  - Search scope, no-large-path reads, no long logs, compaction/clear guidance, and task-packet discipline.
- `templates/agent/policies/testing.md`
  - Bounded test and syntax commands, plus when full tests are appropriate.
- `templates/agent/policies/review-gate.md`
  - Neutral description of doctrine, lead-review gate, hook behavior, advisory mode, and review artifact handling.
- `templates/agent/policies/task-isolation.md`
  - One task per branch/worktree, no cross-task context loading, and handoff requirements.
- `templates/agent/task-packet-template.md`
  - Minimal task packet with branch, objective, safety scope, files allowed, excluded paths, validation commands, and approval gates.
- `templates/CLAUDE.md`
  - Minimal Claude adapter template that points to `AGENTS.md`.
- `templates/codex/README.md`
  - Minimal Codex adapter template that points to `AGENTS.md`.
- `docs/scaffold-test-checklist.md`
  - Exact checklist for copying templates into a target repo and validating them.
- `scripts/render_scaffold.py`
  - Renders templates into a staging directory only, never directly into a target repo.
- `scripts/check_scaffold.py`
  - Checks required scaffold files and unresolved template markers.
- `examples/misalud-lab-lis.values.json`
  - Pilot-specific template values generated from the read-only audit.
- `schemas/agent-telemetry.schema.json` and `docs/telemetry.md`
  - Provider-neutral telemetry schema and privacy rules.

Target repo files to leave unchanged in Phase 1:

- `CLAUDE.md`
- `.claude/`
- `.githooks/`
- `scripts/lead_review.py`
- all app, test, doc, hook, and provider adapter files

Validation:

- Confirm global template files are tracked candidates with `git status --short`.
- Confirm no target repo files changed.
- Confirm `templates/AGENTS.md` references all policy files.
- Render and check the pilot scaffold in a temporary staging directory.
- Do not run the lead review gate yet, because this is documentation-only and the gate costs money.

Checkpoint:

- User reviews the reusable scaffold before approving a copy into `misalud-lab-lis`.

## Phase 2: Scaffold-Test In Pilot Repo

Purpose: copy the global scaffold into `misalud-lab-lis` on an approved branch or worktree, then validate that no safety rule is lost.

Do not start this phase until Phase 2 in `docs/phase-tracker.md` has been reviewed and the user approves a target-repo scaffold test. The plan numbering here is historical; the tracker is the current todo source of truth.

Proposed pilot files to create or modify during the test:

- Modify `CLAUDE.md`
  - Replace canonical policy content with a short adapter that says Claude agents must read `AGENTS.md` first.
  - Keep Claude-specific operational notes only where they are truly Claude-specific.
- Create `.codex/README.md`
  - Codex adapter guidance pointing to `AGENTS.md` and `.agent/`.
  - Notes on avoiding large context rebuilds and using bounded scripts.
- Create `.codex/settings.example.toml` or `.codex/policy.md`
  - Repo-local guidance only, not global Codex config.
- Consider moving `.claude/commands/lead-review.md` into tracked state only if the repo wants provider-specific commands versioned. It is currently ignored, so default is not to track it.

Validation:

- Compare old `CLAUDE.md` against new `AGENTS.md` and ensure no safety rule was lost.
- Confirm `.gitignore` still prevents local settings, PHI, credentials, logs, DBs, and generated artifacts.
- Ask before staging any provider adapter changes.

Checkpoint:

- User approves scaffold-test changes before staging or commit.

## Phase 3: Add Bounded Agent-Facing Scripts

Purpose: reduce prompt/cache churn and prevent accidental large reads.

Proposed pilot files to create:

- `scripts/agent_status.py`
  - Prints branch, dirty files, hook config, Python version, and high-level repo state.
  - Never prints file contents or ignored sensitive files.
- `scripts/agent_diff.py`
  - Wraps `git diff` with the existing lead-review exclude pathspecs.
  - Supports `--stat`, `--name-only`, and bounded unified diff.
- `scripts/agent_test.py`
  - Runs bounded test presets: syntax, targeted pytest, safety tests, full pytest.
  - Defaults to non-production-safe checks only.
- `scripts/agent_policy_check.py`
  - Verifies required policy files exist and provider adapters point to `AGENTS.md`.

Validation:

- Unit-test the scripts where practical.
- Run `python3 -m py_compile scripts/agent_*.py`.
- Run read-only modes only unless the user approves a broader test run.

Checkpoint:

- User approves Phase 3 file list and script behavior before implementation.

## Phase 4: Normalize Review, Security, And Database Skills

Purpose: make reusable skills while preserving the existing Claude review gate.

Proposed control-project deliverables:

- `templates/skills/review.md`
- `templates/skills/security.md`
- `templates/skills/database.md`
- `templates/skills/docs.md`

Proposed pilot changes:

- Reference these skills from `.agent/policies/review-gate.md`.
- Keep `scripts/lead_review.py` Claude-backed until a provider-neutral runner is explicitly designed.

Validation:

- Confirm no new CI, remote, GitHub Action, deploy key, or external automation is introduced.
- Confirm D-1 trigger remains untouched.

Checkpoint:

- User approves any pilot repo references to shared skills.

## Phase 5: Telemetry Schema

Purpose: track cost and cache effectiveness across providers without forcing provider-specific assumptions.

Proposed control-project files:

- `schemas/agent-telemetry.schema.json`
- `docs/telemetry.md`

Status: initial schema and documentation created in Phase 1 global scaffold work.

Proposed fields:

- repo
- task id
- branch
- worktree path
- provider
- model
- session id
- started/ended timestamps
- input tokens
- output tokens
- cache read tokens
- cache write tokens
- cache miss tokens
- total cost
- review cost
- merged PR id
- artifacts

Pilot integration:

- Map existing `scripts/lead_review.py` artifacts into the schema where possible.
- Do not require data the provider does not expose.
- Keep telemetry artifacts ignored unless explicitly approved for tracking.

Validation:

- Validate sample telemetry JSON against schema.
- Confirm telemetry never stores prompts, diffs, PHI, credentials, or raw logs.

Checkpoint:

- User approves telemetry schema before any pilot integration.

## Phase 6: Roll Out To Next Repo

Purpose: turn pilot lessons into a repeatable migration.

Control-project deliverables:

- `docs/rollout-checklist.md`
- `templates/AGENTS.md`
- `templates/CLAUDE.md`
- `templates/codex/README.md`
- `templates/agent/policies/*.md`

Next repo selection criteria:

- Lowest PHI/security risk first, unless the user prefers another high-value repo.
- Repo must be audited read-only before any migration.

## First Approval Request

Approve revised Phase 1 only:

- Create reusable scaffold templates inside `/Users/nicorosen/code_projects/global/agent-dev-system`.
- Do not change `misalud-lab-lis` or any other target repo.
- Do not change existing Claude/Codex behavior in any repo.
- Do not stage or commit without a separate approval.
