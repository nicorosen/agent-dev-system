# Read-Only Audit: misalud-hubspot-exchange

Date: 2026-08-14

Target repo: `/Users/nicorosen/code_projects/misalud/misalud-hubspot-exchange`

Purpose: Next provider-neutral scaffold rollout candidate after `misalud-lab-tracker`.

## Selection

`misalud-hubspot-exchange` is the preferred next rollout target because:

- It is clean on `main`.
- It has no existing `AGENTS.md`, `.agent/`, `CLAUDE.md`, `.claude/`, `.codex/`, or `GEMINI.md`.
- It has a narrow operational domain: local Python scripts for HubSpot CRM export transformation and partner-share CSV preparation.
- Its main safety boundary is clear: do not expose raw CRM exports or full scored contact/company outputs without explicit approval.

`misalud-lab-training` and `misalud-lab-portal` were not selected because both had local changes during triage. `misalud-lab-portal` also already has `.claude/` and needs adapter-aware handling.

No target repo files were modified during this audit.

## Repo State

- Branch: `main`
- Remote: none configured at audit time
- Starting commit: `ef45c39 Add ranking_criteria.md for Fernando`
- Worktree: `/Users/nicorosen/code_projects/misalud/misalud-hubspot-exchange`
- Status at audit:

```text
## main
```

Worktrees:

```text
/Users/nicorosen/code_projects/misalud/misalud-hubspot-exchange  ef45c39 [main]
```

## Provider Files

Found: none.

Not found:

- `AGENTS.md`
- `CLAUDE.md`
- `.agent/`
- `.claude/`
- `.codex/`
- `GEMINI.md`

## Repo Purpose

MiSalud HubSpot Contact Exchange prepares curated HubSpot contact and company lists for Fernando Aguilera under a MindCo Health and MiSALUD referral partner agreement.

The scripts derive relationship warmth from HubSpot exports and write partner-share CSVs. Raw HubSpot exports and full scored outputs are privacy-sensitive and are ignored by git.

## Key Docs

- `README.md`
- `docs/scoring_logic.md`
- `docs/ranking_criteria.md`
- `.gitignore`
- `scripts/build_schema.py`
- `scripts/classify_relationships.py`
- `scripts/classify_companies.py`

## High-Risk Areas

- Raw HubSpot CRM exports in `hubspot_export/`.
- Full scored partner-share outputs:
  - `output/contacts_for_fernando.csv`
  - `output/companies_for_fernando.csv`
- Contact and company PII, relationship scores, and engagement-derived signals.
- Any future HubSpot API upload, email/share action, browser automation, remote sync, or partner-delivery automation.

The audit did not open raw export CSV contents or full scored output CSV contents.

## Default Safe Read Scope

- `README.md`
- `docs/`
- `scripts/`
- `.gitignore`
- `AGENTS.md`
- `.agent/`

Avoid opening:

- `hubspot_export/`
- `output/contacts_for_fernando.csv`
- `output/companies_for_fernando.csv`
- local virtual environments
- editor state
- OS metadata

## Commands

Safe default validation:

```bash
python3 -m py_compile scripts/*.py
python3 /Users/nicorosen/code_projects/global/agent-dev-system/scripts/check_scaffold.py /Users/nicorosen/code_projects/misalud/misalud-hubspot-exchange
```

Approval-gated commands:

```bash
python3 scripts/build_schema.py
python3 scripts/classify_relationships.py
python3 scripts/classify_companies.py
```

These read CRM export data and write output CSVs. Do not run them during scaffold rollout unless the user explicitly approves the data access and output write.

External write operations requiring explicit approval:

- HubSpot API reads or writes.
- Uploading generated CSVs to HubSpot or another CRM.
- Emailing, messaging, or otherwise sharing generated outputs.
- Browser automation over HubSpot or partner systems.
- Adding remote sync or automated partner-delivery behavior.

## Rollout Recommendation

Render the scaffold for inspection, but copy only the first-copy provider-neutral files unless the user approves adapter files:

- `AGENTS.md`
- `.agent/`

Do not copy `CLAUDE.md` or `.codex/` in the first rollout because there are no existing provider adapters to normalize and no remote is configured yet.

Use an isolated worktree or branch. Since no git remote was configured at audit time, push and PR creation are blocked until a remote is added.

## Scaffold Rollout Result

An isolated worktree was created:

- Worktree: `/Users/nicorosen/code_projects/misalud/misalud-hubspot-exchange-agent-provider-neutral-scaffold`
- Branch: `agent/provider-neutral-scaffold-hubspot`
- Base: `main` at `ef45c39`
- Commit: `05aa3bc chore: add provider-neutral agent scaffold`

Copied files:

- `AGENTS.md`
- `.agent/`

Not copied:

- `CLAUDE.md`
- `.codex/`
- app scripts
- docs
- raw HubSpot exports
- full scored output CSVs
- local data, editor state, or OS metadata

Validation:

```text
PASS scaffold valid: /private/tmp/misalud-hubspot-exchange-scaffold
PASS scaffold valid: /Users/nicorosen/code_projects/misalud/misalud-hubspot-exchange-agent-provider-neutral-scaffold
PASS python3 -m py_compile scripts/*.py
PASS git diff --check
```

Blocked:

- Push and PR creation were not possible because the target repo has no configured git remote.
- The local rollout branch is clean and preserved for later remote setup or local merge.
