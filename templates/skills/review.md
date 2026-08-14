# Review Skill Template

Use this skill when reviewing a code change before merge.

## Canonical Policy

- `AGENTS.md`
- `.agent/policies/review-gate.md`
- `.agent/policies/context-budget.md`
- `.agent/policies/testing.md`

Do not duplicate canonical policy in this skill. Use those files as the source of truth for review gates, excluded paths, validation scope, and approval requirements.

## Required Inputs

- Target branch.
- Base branch or commit.
- Repo doctrine or review policy named by `.agent/policies/review-gate.md`.
- Excluded paths from `.agent/policies/context-budget.md`.
- Budget limit for paid or model-backed review.

## Process

1. Read the canonical policy files before inspecting the change.
2. Identify the exact review gate mode: advisory, required, paid, or manually approved.
3. Inspect only the diff and specific surrounding context needed to evaluate it.
4. Use `.agent/bin/agent_diff` or equivalent bounded diff output where available.
5. Report findings first, ordered by severity.

## Finding Bar

A finding needs one of:

- A cited repo doctrine or policy rule.
- A concrete correctness bug with a failure scenario.
- A concrete privacy, security, data-loss, or operational risk.

Do not report style-only issues unless the target repo explicitly gates on style.

## Provider Adapter Guidance

Provider-specific commands, agents, or prompts may call this skill, but they must defer to `AGENTS.md` and `.agent/policies/review-gate.md` for review authority. Keep provider-specific behavior limited to invocation details, model selection, and output formatting.

## Output

- Verdict.
- Findings.
- Coverage limitations.
- Validation run.
- Residual risk.
