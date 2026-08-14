# Documentation Skill Template

Use this skill when adding or changing repo policy, runbooks, architecture docs, or task packets.

## Canonical Policy

- `AGENTS.md`
- `.agent/policies/repo-safety.md`
- `.agent/policies/task-isolation.md`
- `.agent/policies/context-budget.md`

Do not duplicate canonical policy in this skill. Use those files as the source of truth for policy placement, task isolation, excluded paths, and provider-neutral rule precedence.

## Process

1. Identify the canonical source of truth.
2. Avoid duplicating policy across provider adapters.
3. Keep provider-neutral rules in `AGENTS.md` and `.agent/`.
4. Keep provider-specific behavior in provider adapter files.
5. Verify cross-references and paths.

## Provider Adapter Guidance

Provider-specific commands, agents, or prompts may call this skill, but they must keep shared rules in `AGENTS.md` or `.agent/`. Keep provider-specific behavior limited to invocation details, model selection, and output formatting.

## Output

- Files changed.
- Policy moved or added.
- Provider-specific behavior changed, if any.
- Validation performed.
