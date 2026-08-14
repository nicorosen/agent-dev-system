# Review Skill Template

Use this skill when reviewing a code change before merge.

## Required Inputs

- target branch
- base branch or commit
- repo doctrine or review policy
- excluded paths
- budget limit for paid/model-backed review

## Process

1. Read the repo's `AGENTS.md` and `.agent/policies/review-gate.md`.
2. Read the doctrine or review rules named by the target repo.
3. Inspect only the diff and specific surrounding context needed to evaluate it.
4. Exclude large, generated, sensitive, credential-bearing, and raw log paths.
5. Report findings first, ordered by severity.

## Finding Bar

A finding needs one of:

- a cited repo doctrine or policy rule
- a concrete correctness bug with a failure scenario
- a concrete privacy, security, data-loss, or operational risk

Do not report style-only issues unless the target repo explicitly gates on style.

## Output

- verdict
- findings
- coverage limitations
- validation run
- residual risk

