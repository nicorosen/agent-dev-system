# {{REPO_NAME}} Agent Guide

This is the canonical, provider-neutral guide for agents working in this repo. Provider-specific files such as `CLAUDE.md`, `.claude/`, and `.codex/` should adapt to this file rather than redefining repo policy.

## Repo Purpose

{{REPO_PURPOSE}}

## Required Reading

Before making changes, read the relevant policy files:

- `.agent/policies/repo-safety.md`
- `.agent/policies/context-budget.md`
- `.agent/policies/testing.md`
- `.agent/policies/review-gate.md`
- `.agent/policies/task-isolation.md`

Add repo-specific docs here:

- {{REPO_DOCS}}

## Layout

{{REPO_LAYOUT}}

## Default Commands

{{DEFAULT_COMMANDS}}

Only run outward-facing, hardware-facing, production-writing, destructive, or paid-review commands when the user has approved that specific operation.

## Default Search Scope

Search source, tests, scripts, and specific docs by default.

Do not read or search large, generated, ignored, PHI-bearing, credential-bearing, customer-data-bearing, or raw log paths unless the user explicitly asks and the task requires it. The detailed exclusion list is in `.agent/policies/context-budget.md` and `.agent/policies/repo-safety.md`.

## Change Discipline

- Preserve existing safety, security, privacy, and review safeguards.
- Do not weaken ignore rules, hook behavior, doctrine checks, retention rules, audit paths, or redaction protections.
- Do not introduce new remote automation, CI, deploy keys, mirrors, or repo-read integrations without explicit approval and a security review.
- Do not stage, commit, push, or run paid review gates unless the user approves that step.
- If unrelated user changes exist, work around them and do not revert them.

