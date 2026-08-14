# Agent Policy Pack

This directory contains provider-neutral policy for agents working in this repo.

Provider-specific adapters should stay thin:

- `AGENTS.md` is the canonical entrypoint.
- `CLAUDE.md` points Claude Code to `AGENTS.md` and keeps only Claude-specific notes.
- `.claude/` holds Claude-specific agents, commands, and local settings.
- `.codex/` holds Codex-specific guidance.

## Files

- `policies/repo-safety.md`: sensitive data, credentials, external systems, and destructive-operation rules.
- `policies/context-budget.md`: search scope, excluded paths, large-context controls, and task packets.
- `policies/testing.md`: safe default validation commands and escalation rules.
- `policies/review-gate.md`: review doctrine, hooks, and paid-gate behavior.
- `policies/task-isolation.md`: branch, worktree, and handoff discipline.
- `task-packet-template.md`: reusable packet for bounded agent sessions.

## Rule Precedence

Follow direct user instructions first. Then follow `AGENTS.md` and this policy pack. Then follow provider-specific adapter files. If there is a conflict, stop and ask before weakening a safety control.

