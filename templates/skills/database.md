# Database Skill Template

Use this skill when a change touches schema, migrations, persistence, retention, backups, erasure, or data repair.

## Required Reading

- `AGENTS.md`
- `.agent/policies/repo-safety.md`
- target repo data model docs
- target repo retention or erasure docs

## Checks

- Identify the environment and database path before reads or writes.
- Prefer copies for destructive or repair validation.
- Do not dump table contents into agent context.
- Confirm migrations are reversible or explicitly marked irreversible.
- Confirm patient/customer-linked tables have retention, prune, or deletion handling.
- Confirm backups and snapshots are ignored or stored safely.

## Output

- affected tables/files
- safety classification
- migration or repair plan
- validation commands
- rollback or disposal record expectations

