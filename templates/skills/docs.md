# Documentation Skill Template

Use this skill when adding or changing repo policy, runbooks, architecture docs, or task packets.

## Process

1. Identify the canonical source of truth.
2. Avoid duplicating policy across provider adapters.
3. Keep provider-neutral rules in `AGENTS.md` and `.agent/`.
4. Keep provider-specific behavior in provider adapter files.
5. Verify cross-references and paths.

## Output

- files changed
- policy moved or added
- provider-specific behavior changed, if any
- validation performed

