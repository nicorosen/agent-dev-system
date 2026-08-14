# Security Skill Template

Use this skill when a change touches sensitive data, credentials, auth, audit, retention, external systems, or repo access.

## Canonical Policy

- `AGENTS.md`
- `.agent/policies/repo-safety.md`
- `.agent/policies/review-gate.md`
- `.agent/policies/context-budget.md`

Do not duplicate canonical policy in this skill. Use those files as the source of truth for sensitive paths, external writes, credential handling, review gates, and large-context limits.

## Required Reading

- Target repo security review or threat model.
- Target repo security decisions or accepted-risk register.
- Any repo-specific incident response, audit, or retention docs named by `AGENTS.md`.

## Checks

- Does the change create a new sensitive-data surface?
- Does it alter credential storage, credential flow, or URL handling?
- Does it add repo-read automation, CI, deploy keys, remotes, mirrors, or collaborators?
- Does it change logging, exceptions, telemetry, or review artifacts?
- Does it change retention, pruning, deletion, or audit behavior?
- Does it write to production or external systems?

## Provider Adapter Guidance

Provider-specific commands, agents, or prompts may call this skill, but they must not weaken `AGENTS.md` or `.agent/policies/repo-safety.md`. Keep provider-specific behavior limited to invocation details, model selection, and output formatting.

## Output

- Risk summary.
- Required policy or doc updates.
- Tests or verification needed.
- Approval gates before external writes or merge.
