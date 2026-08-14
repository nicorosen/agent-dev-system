# Security Skill Template

Use this skill when a change touches sensitive data, credentials, auth, audit, retention, external systems, or repo access.

## Required Reading

- `AGENTS.md`
- `.agent/policies/repo-safety.md`
- target repo security review or threat model
- target repo security decisions or accepted-risk register

## Checks

- Does the change create a new sensitive-data surface?
- Does it alter credential storage, credential flow, or URL handling?
- Does it add repo-read automation, CI, deploy keys, remotes, mirrors, or collaborators?
- Does it change logging, exceptions, telemetry, or review artifacts?
- Does it change retention, pruning, deletion, or audit behavior?
- Does it write to production or external systems?

## Output

- risk summary
- required policy/doc updates
- tests or verification needed
- approval gates before external writes or merge

