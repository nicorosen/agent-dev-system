# Database Skill Template

Use this skill when a change touches schema, migrations, persistence, retention, backups, erasure, or data repair.

## Canonical Policy

- `AGENTS.md`
- `.agent/policies/repo-safety.md`
- `.agent/policies/testing.md`
- `.agent/policies/context-budget.md`

Do not duplicate canonical policy in this skill. Use those files as the source of truth for sensitive data, safe validation commands, excluded paths, and approval requirements.

## Required Reading

- Target repo data model docs.
- Target repo retention or erasure docs.
- Target repo migration, backup, or repair runbooks named by `AGENTS.md`.

## Checks

- Identify the environment and database path before reads or writes.
- Prefer copies for destructive or repair validation.
- Do not dump table contents into agent context.
- Confirm migrations are reversible or explicitly marked irreversible.
- Confirm patient/customer-linked tables have retention, prune, or deletion handling.
- Confirm backups and snapshots are ignored or stored safely.

## Provider Adapter Guidance

Provider-specific commands, agents, or prompts may call this skill, but they must defer to `AGENTS.md` and `.agent/policies/repo-safety.md` for database safety controls. Keep provider-specific behavior limited to invocation details, model selection, and output formatting.

## Output

- Affected tables or files.
- Safety classification.
- Migration or repair plan.
- Validation commands.
- Rollback or disposal record expectations.
