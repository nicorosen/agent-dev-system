# Repo Rollout Checklist

Use this checklist for each repo after the global scaffold has been validated.

## 1. Select Target

- [ ] Identify target repo path.
- [ ] Confirm why this repo is next.
- [ ] Confirm whether the repo handles PHI, credentials, customer data, hardware, external writes, or production state.
- [ ] Confirm no target repo changes will happen during audit.

## 2. Read-Only Audit

- [ ] Record current branch.
- [ ] Record dirty files.
- [ ] Record worktrees.
- [ ] Locate provider files: `AGENTS.md`, `CLAUDE.md`, `.claude/`, `.codex/`, `.agent/`, `GEMINI.md`.
- [ ] Locate repo policy docs, security docs, runbooks, hooks, and test docs.
- [ ] Locate ignore rules and high-risk generated/sensitive paths without opening sensitive files.
- [ ] Locate scripts and tests relevant to safety, review, status, diff, and validation.
- [ ] Record current agent/provider behavior.

## 3. Generate Values

- [ ] Create `examples/<repo>.values.json` in this global project.
- [ ] Fill every key from `schemas/scaffold-values.schema.json`.
- [ ] Keep values high signal and repo-specific.
- [ ] Do not include PHI, credentials, raw logs, raw diffs, or secret paths with values.

## 4. Render To Staging

Run from the global project:

```bash
python3 scripts/render_scaffold.py \
  --values examples/<repo>.values.json \
  --out /private/tmp/<repo>-scaffold \
  --include-provider-adapters \
  --force
python3 scripts/check_scaffold.py /private/tmp/<repo>-scaffold
```

- [ ] Inspect staged file list.
- [ ] Inspect rendered `AGENTS.md`.
- [ ] Inspect rendered `.agent/`.
- [ ] Inspect provider adapters only if adapter testing is approved.

## 5. Approval Before Copy

Ask the user to approve:

- [ ] target repo path
- [ ] branch or worktree strategy
- [ ] exact files to create or modify
- [ ] whether provider adapters are included
- [ ] whether staging, committing, or pushing is allowed

Do not copy anything before approval.

## 6. Copy Into Target Repo

- [ ] Confirm branch and dirty files again.
- [ ] Copy only approved files.
- [ ] Do not touch app code, tests, hooks, ignored local settings, generated files, data files, or credentials unless explicitly approved.

## 7. Validate Target Repo

- [ ] Run `python3 <global-project>/scripts/check_scaffold.py <target-repo>`.
- [ ] Confirm `git status --short --branch`.
- [ ] Confirm no ignored/sensitive/generated paths are staged.
- [ ] Confirm provider adapters point to `AGENTS.md`.
- [ ] Confirm old provider policy was not lost.
- [ ] Do not run paid review gates unless explicitly approved.

## 8. Stop For Review

Report:

- [ ] files changed
- [ ] validation run
- [ ] validation not run
- [ ] safety controls preserved
- [ ] any follow-up needed

Stop before staging, committing, pushing, or moving to another repo unless explicitly approved.

