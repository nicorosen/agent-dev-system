# Agent Telemetry

Telemetry records provider cost and cache behavior without storing prompts, raw diffs, logs, PHI, credentials, or customer data.

## Goals

- Compare provider cost per task and merged PR.
- Track cache effectiveness where a provider exposes cache reads and writes.
- Identify costly workflows caused by repeated context rebuilds.
- Preserve privacy and security boundaries.

## Storage Rule

Telemetry files are generated artifacts. Keep raw exports out of git unless a repo explicitly approves sanitized aggregate samples.

Recommended ignored locations in target repos:

- `.agent/telemetry/raw/`
- `artifacts/agent-telemetry/`

## Required Fields

Each record should include:

- `schema_version`
- `repo`
- `task_id`
- `provider`
- `started_at`

Every other metric is optional because providers expose different usage fields.

## Provider Mapping

Use provider-native fields when available:

- Claude Code review artifacts may expose `total_cost_usd` and `session_id`.
- OpenAI usage APIs may expose input, output, cached, and reasoning-token fields depending on the surface.
- Some tools expose no cost or cache fields. Record `null` rather than estimating.

## Privacy Rules

Never store:

- prompts
- model responses
- raw diffs
- stack traces with sensitive data
- database rows
- patient, customer, or credential values
- log excerpts
- local filesystem secrets

Use references instead:

- commit SHA
- branch name
- PR number
- sanitized artifact path
- aggregate counts

## Cost Metrics

Recommended derived metrics:

- cache hit ratio: `cache_read_tokens / input_tokens`
- cache write ratio: `cache_write_tokens / input_tokens`
- cost per session: `total_cost_usd`
- cost per task: sum by `task_id`
- cost per merged PR: sum by `merged_pr.id`

Derived metrics should tolerate missing provider data.

