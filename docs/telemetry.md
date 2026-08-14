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
  - Map `total_cost_usd` to `cost.total_cost`.
  - Map review-only spend to `cost.review_cost` when the artifact represents a review gate.
  - Map Claude session identifiers to `session_id`.
  - Map missing token or cache fields to `null`.
- OpenAI/Codex usage surfaces may expose input, output, cached, and reasoning-token fields depending on the API surface.
  - Map input tokens to `usage.input_tokens`.
  - Map output tokens to `usage.output_tokens`.
  - Map cached input tokens to `usage.cache_read_tokens` when exposed as cache reads.
  - Map cache creation/write tokens to `usage.cache_write_tokens` when exposed.
  - Map reasoning tokens to `usage.reasoning_tokens` when exposed.
  - Map missing cost, cache, or token fields to `null`.
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

## Validation Command

Validate a telemetry file or directory of `.json` records:

```bash
python3 scripts/validate_telemetry.py examples/telemetry
```

The command checks the schema-required fields, rejects forbidden raw-content fields, requires referenced artifacts to be marked sanitized, and prints aggregate task and merged-PR metrics.

## Fixture Examples

Sanitized examples live in `examples/telemetry/`:

- `claude-review.json`: Claude-style review session with cost and cache fields.
- `openai-codex-task.json`: OpenAI/Codex-style task session with partial usage fields and nulls for missing provider data.
