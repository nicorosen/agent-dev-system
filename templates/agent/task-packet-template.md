# Task Packet

## Objective

{{OBJECTIVE}}

## Repo State

- Repo: {{REPO}}
- Branch: {{BRANCH}}
- Worktree: {{WORKTREE}}
- Starting commit: {{STARTING_COMMIT}}
- Dirty files: {{DIRTY_FILES}}

## Allowed Scope

- Files allowed: {{FILES_ALLOWED}}
- Directories allowed: {{DIRECTORIES_ALLOWED}}
- Files explicitly off-limits: {{FILES_OFF_LIMITS}}
- External systems allowed: {{EXTERNAL_SYSTEMS_ALLOWED}}

## Safety Notes

- Sensitive-data risk: {{SENSITIVE_DATA_RISK}}
- Credential risk: {{CREDENTIAL_RISK}}
- Production-write risk: {{PRODUCTION_WRITE_RISK}}
- Hardware risk: {{HARDWARE_RISK}}
- Automation or repo-read integration risk: {{AUTOMATION_RISK}}

## Required Reading

- `AGENTS.md`
- `.agent/policies/repo-safety.md`
- `.agent/policies/context-budget.md`
- `.agent/policies/testing.md`
- `.agent/policies/review-gate.md`
- `.agent/policies/task-isolation.md`

Task-specific docs:

- {{TASK_SPECIFIC_DOCS}}

## Plan

{{PLAN}}

## Validation

Commands to run:

```bash
{{VALIDATION_COMMANDS}}
```

Expected evidence:

- {{EXPECTED_EVIDENCE}}

## Approval Checkpoints

- Before edits: {{APPROVAL_BEFORE_EDITS}}
- Before external writes: {{APPROVAL_BEFORE_EXTERNAL_WRITES}}
- Before staging: {{APPROVAL_BEFORE_STAGING}}
- Before commit: {{APPROVAL_BEFORE_COMMIT}}
- Before push: {{APPROVAL_BEFORE_PUSH}}

## Completion Notes

- Files changed: {{FILES_CHANGED}}
- Validation run: {{VALIDATION_RUN}}
- Validation not run: {{VALIDATION_NOT_RUN}}
- Follow-up needed: {{FOLLOW_UP_NEEDED}}

