# Context Budget Policy

Keep agent context bounded and stable so provider prompt caching can work and sensitive data does not leak into prompts.

## Default Read Scope

Search and read these paths first:

- {{DEFAULT_READ_SCOPE}}

Use precise searches before reading whole files. Prefer targeted line ranges over full dumps.

## Excluded By Default

Do not read or search these unless explicitly asked and needed:

- {{EXCLUDED_PATHS}}

If a task requires one of these paths, state why, read the smallest possible slice, and avoid copying sensitive contents into the conversation.

## Large Output Rules

- Do not dump whole DB tables, full logs, large diffs, or generated files into context.
- For searches, report relevant filenames and line numbers first.
- For diffs, prefer `--stat`, `--name-only`, or narrowly scoped hunks.
- For test failures, include the failing test names and concise error context, not full logs.

## Session Hygiene

- Keep one task per session, branch, or worktree where practical.
- Use task packets for handoffs or long-running work.
- Suggest compaction at natural task boundaries or when the thread becomes large.
- Suggest clearing context when switching to an unrelated task.
- Do not carry unrelated repo history into a new task packet.

