# Codex Adapter

Read `AGENTS.md` first. It is the canonical provider-neutral policy for this repo.

Then read any task-relevant files under `.agent/`.

Codex-specific notes:

- Keep local edits scoped to approved files.
- Use bounded commands and targeted reads to preserve context efficiency.
- Do not copy raw logs, sensitive data, credentials, or large generated output into chat.
- Do not re-state or override safety policy from `AGENTS.md`.
- If `AGENTS.md` and this file disagree, follow `AGENTS.md` unless the user explicitly says otherwise.

