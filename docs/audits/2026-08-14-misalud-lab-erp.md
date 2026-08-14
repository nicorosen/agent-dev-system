# Read-Only Audit: misalud-lab-erp

Date: 2026-08-14

Target repo: `/Users/nicorosen/code_projects/misalud/misalud-lab-erp`

Purpose: Phase 7 candidate for provider-neutral agent scaffold rollout.

## Selection

`misalud-lab-erp` is the preferred next rollout target over `misalud-lab-tracker` because:

- It has no `AGENTS.md`, `.agent/`, `CLAUDE.md`, `.codex/`, or `GEMINI.md` yet.
- It has a narrow operational domain: ERPNext procurement, stock, assets, and event planning.
- It has clear high-risk controls around live ERPNext/Frappe Cloud writes.
- `misalud-lab-tracker` already has `AGENTS.md`, `CLAUDE.md`, `.claude/`, and `.codex/`, and needs a separate adapter-normalization pass rather than a first scaffold rollout.

No target repo files were modified during this audit.

## Repo State

- Branch: `main`
- Remote: `origin https://github.com/nicorosen/misalud-lab-erp.git`
- Starting commit: `2807543`
- Status at audit:

```text
## main...origin/main
 M .scripts/erpnext-v1-masters.ts
 M .scripts/erpnext-v1-migrate-history.ts
 M .scripts/erpnext-v1-verify.ts
 M .scripts/fetch-live-sheet.py
 M .scripts/lib/event-plan.test.ts
 M .scripts/lib/po-migration.test.ts
 M .scripts/lib/tracker-xlsx.test.ts
 M .scripts/lib/tracker-xlsx.ts
 M .scripts/package.json
 M README.md
 M procurement/migration/RUNBOOK.md
?? .scripts/erpnext-wave-diff.ts
```

Existing local changes must be preserved. Any rollout should use a new worktree or wait until the current dirty work is resolved.

Worktrees:

```text
/Users/nicorosen/code_projects/misalud/misalud-lab-erp                                                  2807543 [main]
/Users/nicorosen/code_projects/misalud/misalud-lab-erp.worktrees/agents-erp-migration-completion-check  5dac437 [agents/erp-migration-completion-check] prunable
```

## Provider Files

Found:

- `.claude/`
- tracked `.claude/.gmail-token.json`
- tracked `.claude/context/procurement.md`

Not found:

- `AGENTS.md`
- `CLAUDE.md`
- `.agent/`
- `.codex/`
- `GEMINI.md`

Local credential files seen in the file tree but not opened:

- `.claude/.env.local`
- `.claude/google_sheets_token.json`

## Repo Purpose

MiSalud Lab ERP manages ERPNext v16 on Frappe Cloud for procurement, stock, assets, Purchase Orders, receipts, invoices, payments, and event planning. It is progressively replacing the `Procurement_Tracker` Google Sheet.

## Key Docs

- `README.md`
- `procurement/migration/RUNBOOK.md`
- `procurement/ERP-OPERATOR-MANUAL.md`
- `operations/erp/erpnext-stage-roadmap.md`
- `compliance/operis/operis-erpnext-boundary.md`
- `compliance/sops/SOP-013_procurement_and_intercompany.md`

Archived docs under `docs/archive/` are superseded and should not drive rollout policy.

## High-Risk Areas

- Live ERPNext/Frappe Cloud writes to `https://misalud.v.frappe.cloud`.
- Google Sheets reads and writes against procurement tracker data.
- Credential files under `.claude/`.
- Excel snapshots in `procurement/migration/`, including working and cutover snapshots.
- Destructive reset command: `npm run erpnext:v1-reset`.
- Wave migration scripts that write ERPNext masters, POs, receipts, assets, BOMs, and Event Plans.
- Frappe/ERPNext private, public, logs, backups, locks, config, and bench paths if present.

## Default Safe Read Scope

- `README.md`
- `procurement/migration/RUNBOOK.md`
- `procurement/ERP-OPERATOR-MANUAL.md`
- `operations/erp/`
- `compliance/`
- `.scripts/` source and tests, excluding credential files and generated dependencies

Avoid opening:

- `.claude/.env.local`
- `.claude/.gmail-token.json`
- `.claude/google_sheets_token.json`
- `procurement/migration/*.xlsx`
- `node_modules/`
- ERPNext private, public, log, backup, lock, config, and bench directories

## Commands

Safe default validation:

```bash
cd .scripts && npm test
cd .scripts && npm run erpnext:wave-diff
```

External-write or destructive commands requiring explicit approval:

```bash
cd .scripts && npm run erpnext:v1-masters
cd .scripts && SYNC_WAVE=1 npm run erpnext:v1-sync
cd .scripts && npm run erpnext:v1-assets
cd .scripts && npm run erpnext:v1-verify
cd .scripts && npm run erpnext:v1-reset
```

`erpnext:v1-reset` must not be run against the live instance except under a separately approved disaster-recovery or cutover procedure.

## Rollout Recommendation

Render the scaffold for inspection only, with provider adapters included in staging. Do not copy into the target repo until the user approves:

- a new worktree path and branch,
- exact file list,
- how to handle the existing `.claude/` directory,
- whether to add `CLAUDE.md` and `.codex/README.md`,
- staging, committing, and pushing.

Given the current dirty main checkout, do not copy scaffold files into `/Users/nicorosen/code_projects/misalud/misalud-lab-erp` directly.

## Scaffold Rollout Result

After the main checkout was confirmed clean, an isolated worktree was created:

- Worktree: `/Users/nicorosen/code_projects/misalud/misalud-lab-erp-agent-provider-neutral-scaffold`
- Branch: `agent/provider-neutral-scaffold-erp`
- Base: `main` at `a6373a8`
- Commit: `2ef4eee chore: add provider-neutral agent scaffold`
- PR: `https://github.com/nicorosen/misalud-lab-erp/pull/1`

Copied files:

- `AGENTS.md`
- `.agent/`

Not copied:

- `CLAUDE.md`
- `.codex/`
- `.claude/`
- app scripts
- docs
- credentials
- snapshots
- generated files

Validation:

```text
PASS scaffold valid: /Users/nicorosen/code_projects/misalud/misalud-lab-erp-agent-provider-neutral-scaffold
```

PR state after creation:

- Open
- Mergeable
- 1 commit
- 12 changed files
- 562 additions

## Merge And Cleanup

PR #1 was merged into `main`.

- Merge commit: `2affb5b`
- Local `main` fast-forwarded to `origin/main`.
- Remote branch `agent/provider-neutral-scaffold-erp` deleted.
- Local branch `agent/provider-neutral-scaffold-erp` deleted.
- Temporary worktree removed.

Final validation:

```text
PASS scaffold valid: /Users/nicorosen/code_projects/misalud/misalud-lab-erp
```
