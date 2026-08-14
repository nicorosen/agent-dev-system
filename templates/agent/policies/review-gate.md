# Review Gate Policy

This repo may have local, remote, human, or model-backed review gates. Treat those gates as safety controls.

## Doctrine

Repo-specific doctrine source:

- {{DOCTRINE_SOURCE}}

Security decisions source:

- {{SECURITY_DECISIONS_SOURCE}}

## Hook State

Document local hook configuration here:

- {{HOOK_STATE}}

## Paid Or Model-Backed Review

Paid or model-backed review gates require explicit user approval unless the repo policy says otherwise.

The review implementation should:

- exclude large and sensitive paths
- enforce budget, file-count, and diff-size controls
- avoid storing prompts, raw diffs, sensitive data, credentials, or long logs
- record cost and session IDs only when the provider exposes them
- cache byte-identical review results when safe

## Review Findings

Findings should cite repo doctrine, policy IDs, or concrete correctness failures. Do not treat style, formatting, naming, import ordering, or type-annotation completeness as defects unless a repo rule explicitly makes them relevant.

