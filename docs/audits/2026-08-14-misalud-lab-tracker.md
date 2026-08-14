# Read-Only Audit: misalud-lab-tracker

Date: 2026-08-14

Target repo: `/Users/nicorosen/code_projects/misalud/misalud-lab-tracker`

Purpose: Follow-up provider-neutral scaffold rollout candidate after `misalud-lab-erp`.

## Selection

`misalud-lab-tracker` is a follow-up rollout candidate, but it is not a first-copy scaffold case. It already has:

- `AGENTS.md`
- `CLAUDE.md`
- `.claude/`
- `.codex/`

The right next step is adapter normalization: add the shared `.agent/` policy pack and update the existing `AGENTS.md`/adapters carefully, preserving the current build, bilateral sync, and compliance-document controls.

No target repo files were modified during this audit.

## Repo State

- Branch: `main`
- Starting commit: `276244e2`
- Worktree: `/Users/nicorosen/code_projects/misalud/misalud-lab-tracker`
- Status at audit:

```text
## main...origin/main
 M .plans/i-need-to-unify-elegant-mango.md
 M .scripts/lib/gmail-client.ts
 M compliance/change-reports/INDEX.md
 M compliance/sops/changelogs/sop_007_result_reporting.md
 M compliance/sops/sop_007_result_reporting.md
 M compliance/templates/standing-physician-order.md
?? .plans/let-s-review-the-vaccination-golden-lovelace.md
?? .plans/re-hc-triple-role-snuggly-marble.md
?? .plans/read-the-following-rfi-silly-bumblebee.md
?? compliance/change-reports/CR-2026-08-05-sop_007_result_reporting.md
```

Existing local changes must be preserved. Do not copy scaffold files into the main checkout while it is dirty.

Worktrees:

```text
/Users/nicorosen/code_projects/misalud/misalud-lab-tracker  276244e2 [main]
/Users/nicorosen/code_projects/misalud-command-center       702c4b14 [command-center] prunable
```

## Provider Files

Tracked:

- `AGENTS.md`
- `CLAUDE.md`
- `.claude/` commands, agents, skills, context, settings, hooks, state files
- `.codex/` agents, config, hooks

Not found:

- `.agent/`
- `GEMINI.md`

Credential or local-state paths seen in the file tree but not opened:

- `.claude/.env.local`
- `.claude/.gmail-token.json`
- `.claude/.scan-state.json`
- `.claude/settings.local.json`
- `.claude/tmp/`

## Current Adapter Notes

`AGENTS.md` currently contains useful repo policy, but it refers to `.Codex/` paths while the tracked provider directory is `.codex/` and the existing Claude content uses `.claude/`. It also does not yet delegate to `.agent/policies/*`.

`CLAUDE.md` is detailed and provider-specific. It contains build/release commands, script commands, architecture notes, bilateral sync rules, LIS handoff guidance, task management, and business context. It should not be replaced blindly.

`.codex/hooks/pre-edit-sync-check.sh` mirrors the bilateral sync guard and blocks edits to content sources when Drive artifacts are newer. Compliance paths cannot be bypassed.

## Repo Purpose

MiSalud Lab Tracker is the source-driven operations and compliance tracker for the lab launch. It contains Markdown and CSV source documents for execution, regulatory, procurement, staffing, compliance, location, operations, commercial, and product integration work. Release artifacts are built to Google Drive.

## Key Docs

- `AGENTS.md`
- `CLAUDE.md`
- `README.md`
- `README-setup.md`
- `compliance/README.md`
- `execution/task_board.csv`
- `.scripts/lib/bilateral-sync.ts`
- `.codex/hooks/pre-edit-sync-check.sh`
- `.claude/hooks/pre-edit-sync-check.sh`

## High-Risk Areas

- Compliance SOPs and change reports.
- Bilateral sync between source files and Google Drive release artifacts.
- Google Drive symlinks such as `assets`, `regulatory/context`, and `staffing/context`.
- Credential-bearing `.claude/` files.
- Plane, Gmail, Supabase, Neon, Google Sheets, Playwright, Slack, and other external-system automation.
- Release builds that write DOCX, XLSX, PDF, PPTX, dashboards, graph files, or Google Drive outputs.
- Compliance reverse-sync and document-control workflows.

## Default Safe Read Scope

- `AGENTS.md`
- `CLAUDE.md`
- `README.md`
- `.codex/hooks.json`
- `.codex/hooks/pre-edit-sync-check.sh`
- `.scripts/` source and tests, excluding generated dependencies and credentials
- relevant docs under `execution/`, `regulatory/`, `procurement/`, `staffing/`, `compliance/`, `location/`, `operations/`, `commercial/`, and `product-integration/`

Avoid opening:

- `.claude/.env.local`
- `.claude/.gmail-token.json`
- `.claude/.scan-state.json`
- `.claude/settings.local.json`
- `.claude/tmp/`
- `node_modules/`
- `.scripts/node_modules/`
- generated release outputs
- Google Drive symlink targets unless explicitly needed

## Commands

Safe default validation:

```bash
cd .scripts && npm test
make list
```

Approval-gated commands:

```bash
make release
make release-all
make dashboard
make serve
npx tsx .scripts/plane-ops.ts sync
npx tsx .scripts/cola-kb.ts search "topic"
npx tsx .scripts/lib/bilateral-sync.ts scan
```

Any command that sends email, writes Plane, writes Google Sheets, writes Supabase/Neon, updates Google Drive artifacts, runs browser automation, or changes compliance controlled docs needs explicit approval.

## Rollout Recommendation

Do not do a direct scaffold overwrite. Recommended next path:

1. Wait for or create a clean isolated worktree.
2. Render the tracker scaffold to staging.
3. Compare current `AGENTS.md` and `CLAUDE.md` against staged `AGENTS.md`, `.agent/`, and provider adapters.
4. Copy `.agent/` first.
5. Update `AGENTS.md` by preserving tracker-specific policy and adding references to `.agent/policies/*`.
6. Leave `.claude/` and `.codex/` intact except for narrow adapter references approved separately.

## Normalization Result

After the main checkout was confirmed clean, an isolated worktree was created:

- Worktree: `/Users/nicorosen/code_projects/misalud/misalud-lab-tracker-agent-policy-normalization`
- Branch: `agent/normalize-agent-policy`
- Base: `main` at `8bbe0917`
- Commit: `dc1d937f Meta Add: provider-neutral agent policy pack`
- PR: `https://github.com/nicorosen/misalud-lab-tracker/pull/3`

Copied or changed files:

- `.agent/`
- `AGENTS.md` with a narrow provider-neutral policy-pack entrypoint and required `.agent/policies/*` references

Not changed:

- `CLAUDE.md`
- `.claude/`
- `.codex/`
- app scripts
- compliance source docs
- credentials
- release artifacts
- Google Drive symlink targets

Validation:

```text
PASS scaffold valid: /Users/nicorosen/code_projects/misalud/misalud-lab-tracker-agent-policy-normalization
```

Full tracker script tests were run in the normalization worktree and on clean `main`. Both showed the same existing baseline failures:

- `lib/dep-graph.test.ts`: `daysToLaunch` is now `-100`, expected greater than 0.
- `lib/milestones.test.ts`: three milestone/progress threshold failures.
- Baseline result on clean `main`: 142 passed, 4 failed.

PR state after creation:

- Open
- Mergeable
- 1 commit
- 12 changed files
- 525 additions

## Merge and Cleanup Result

PR #3 was merged on 2026-08-14:

- PR: `https://github.com/nicorosen/misalud-lab-tracker/pull/3`
- Merge commit: `f4c64772d2fc4044a300adb1a320fb4df542b7a1`
- Feature commit: `dc1d937f609ddb2340422a936b749856297f3b27`
- Remote feature branch: deleted by merge

Local cleanup completed:

- Tracker main checkout fast-forwarded to `f4c64772`
- Removed worktree: `/Users/nicorosen/code_projects/misalud/misalud-lab-tracker-agent-policy-normalization`
- Deleted local branch: `agent/normalize-agent-policy`
- Confirmed tracker main status: `## main...origin/main`

## Provider Adapter Normalization Result

After PR #3 landed, a second isolated worktree was created:

- Worktree: `/Users/nicorosen/code_projects/misalud/misalud-lab-tracker-provider-adapter-normalization`
- Branch: `agent/normalize-provider-adapters`
- Base: `main` at `f4c64772`
- Commit: `f099440f Meta Update: normalize provider adapter references`
- PR: `https://github.com/nicorosen/misalud-lab-tracker/pull/4`

Changed files:

- `AGENTS.md`: replaced stale `.Codex` path references with the actual `.claude/` context paths, `.codex/` hook path, and provider-specific MCP config locations.
- `CLAUDE.md`: added a narrow provider-neutral policy pointer to `AGENTS.md` and fixed one unqualified `workflows.md` reference.
- `.codex/agents/pm-analyst.toml`: replaced stale `.Codex/context` references with `.claude/context`.

Not changed:

- `.claude/` commands, skills, hooks, local state, and credentials.
- `.codex/` settings and hooks, except the `pm-analyst` agent documentation string.
- App scripts, compliance source docs, release artifacts, sync automation, and Google Drive symlink targets.

Validation:

```text
PASS agent policy scaffold valid: /Users/nicorosen/code_projects/misalud/misalud-lab-tracker-provider-adapter-normalization
PASS git diff --check
PASS stale reference scan for .Codex, ~/.Codex, and "See workflows.md"
PASS referenced context and hook file existence checks
```

Full tracker script tests were run after installing `.scripts` dependencies in the worktree. They showed the same existing baseline failures as PR #3 validation:

- `lib/dep-graph.test.ts`: `daysToLaunch` is now `-100`, expected greater than 0.
- `lib/milestones.test.ts`: three milestone/progress threshold failures.
- Result: 142 passed, 4 failed.

PR #4 state after creation:

- Open
- Draft
- Mergeable
- CodeRabbit: success
- 1 commit

## Provider Adapter Merge and Cleanup Result

PR #4 was marked ready and merged on 2026-08-14:

- PR: `https://github.com/nicorosen/misalud-lab-tracker/pull/4`
- Merge commit: `8fafb2bea38b97567c2bba868ebf834be75179ed`
- Feature commit: `f099440fecbbe987e1b65bb10418dadd284f8603`
- Remote feature branch: deleted by merge

Local cleanup completed:

- Tracker main checkout fast-forwarded to `8fafb2be`
- Removed worktree: `/Users/nicorosen/code_projects/misalud/misalud-lab-tracker-provider-adapter-normalization`
- Deleted local branch: `agent/normalize-provider-adapters`
- Confirmed tracker main status: `## main...origin/main`
