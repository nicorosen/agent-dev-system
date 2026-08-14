# Repo Safety Policy

Default to the safest interpretation when a command can read sensitive data, expose credentials, write to production state, call external systems, or interact with hardware.

## Sensitive Data And Credentials

Do not read, print, summarize, copy, stage, commit, or upload sensitive-data-bearing or credential-bearing files unless the user explicitly authorizes that exact operation.

Repo-specific high-risk paths:

- {{HIGH_RISK_PATHS}}

Ignore rules can be safety controls. Do not add unignore exceptions for sensitive paths without explicit approval and a security rationale.

## Production Writes

Before touching data paths, identify the resolver or config source of truth and state which path or environment is being used.

External-write operations require explicit user approval:

- {{EXTERNAL_WRITE_OPERATIONS}}

## Security Doctrine

Preserve existing repo doctrine and review gates, especially:

- no sensitive data in logs, exceptions, status output, telemetry, or review artifacts
- no credentials in tracked files, URLs, logs, command output, or task packets
- no new sensitive-data surface without updating the repo's surface inventory
- no new automation with repo read access without security review

## Git Safety

Do not revert unrelated user work. Do not use destructive git commands unless the user explicitly asks for them. Do not stage or commit ignored local settings, data exports, logs, databases, generated build output, or review artifacts.

