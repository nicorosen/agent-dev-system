# Task Isolation Policy

Keep each agent session scoped to one task. This protects user work, keeps context smaller, and makes prompt caching more effective.

## Branch And Worktree Rules

- Prefer one branch or worktree per task.
- Before edits, check current branch and dirty status.
- If unrelated uncommitted work exists, do not revert it.
- If a task needs broad code changes, propose an isolated worktree before editing.
- If working in place, keep file edits limited to the approved scope.

## Task Packets

Use `.agent/task-packet-template.md` for long-running work, handoffs, or parallel task execution.

A task packet should name:

- objective
- branch or worktree
- allowed files
- excluded paths
- safety risks
- validation commands
- approval checkpoints
- completion evidence

## Handoffs

When handing work to another agent or session:

- include the exact current branch
- include dirty files
- include files changed by this task
- include validation already run and validation still needed
- do not include sensitive data, credentials, long logs, full database rows, or large diffs

## Stop Conditions

Stop and ask before proceeding if:

- a task requires sensitive-data or credential-bearing files
- a task needs production writes or external-system writes
- a change would weaken safety policy
- a change would introduce new repo-read automation, CI, deploy keys, remotes, or mirrors
- unrelated user changes make the requested edit ambiguous

