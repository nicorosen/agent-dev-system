# Claude Adapter

Read `AGENTS.md` first. It is the canonical provider-neutral policy for this repo.

Then read any task-relevant files under `.agent/`.

Claude-specific notes:

- Keep context bounded. Prefer targeted reads and searches over full-file dumps.
- Do not re-state or override safety policy from `AGENTS.md`.
- If `AGENTS.md` and this file disagree, follow `AGENTS.md` unless the user explicitly says otherwise.

