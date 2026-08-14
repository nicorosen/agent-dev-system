# Agent Development System Phase Tracker

Use this as the persistent todo list for the provider-neutral agent development system.

## Phase Summary

- [x] Phase 0: Create control project and audit pilot repo
- [x] Phase 1: Build provider-neutral scaffold in global project
- [x] Phase 2: Harden scaffold and rollout process
- [x] Phase 3: Scaffold-test in `misalud-lab-lis`
- [x] Phase 4: Add bounded agent-facing scripts
- [x] Phase 5: Normalize reusable skills
- [x] Phase 6: Finalize telemetry and reporting
- [ ] Phase 7: Roll out to the next repo

## Model Guidance

Use the cheapest model that can safely complete the phase. Escalate only when the phase involves security/HIPAA equivalence, provider adapter behavior, review-gate logic, or ambiguous repo-specific policy.

| Phase | Recommended model tier | Why |
|---|---|---|
| Phase 0: Audit | High or medium-high reasoning | Read-only audit must preserve security, HIPAA, hook, and provider-policy details. |
| Phase 1: Global scaffold | Medium reasoning | Template design benefits from coherent abstraction, but no target repo edits. |
| Phase 2: Scaffold hardening | Medium reasoning | Values contract, tests, and rollout controls need careful design but are contained. |
| Phase 3: Pilot scaffold test | Cheap or medium reasoning | Copying `AGENTS.md` and `.agent/` plus validation is mostly mechanical. Escalate if comparing safety policies gets ambiguous. |
| Phase 4: Bounded scripts | Medium reasoning | Script behavior affects future agent safety and should be designed carefully. |
| Phase 5: Reusable skills | Medium-high reasoning | Skills shape future review/security/database behavior across repos. |
| Phase 6: Telemetry | Cheap or medium reasoning | Schema/reporting work is contained. Escalate only for provider-specific cost/cache mapping. |
| Phase 7: Next repo rollout | Medium reasoning by default | Start medium for repo audit and scaffold copy. Escalate for high-risk repos or policy conflicts. |

Current recommendation: continue Phase 7 with medium reasoning for the next repo audit and rollout planning.

## Phase 0: Create Control Project And Audit Pilot Repo

Status: complete

Done:

- Created `/Users/nicorosen/code_projects/global/agent-dev-system`.
- Performed read-only audit of `/Users/nicorosen/code_projects/misalud/misalud-lab-lis`.
- Captured audit in `docs/audits/2026-08-14-misalud-lab-lis.md`.
- Confirmed target repos should stay untouched until scaffold test or rollout.

## Phase 1: Build Provider-Neutral Scaffold In Global Project

Status: complete

Done:

- Added provider-neutral templates under `templates/`.
- Added Claude and Codex thin adapter templates.
- Added `.agent/` policy templates.
- Added reusable skill templates.
- Added telemetry schema and docs.
- Added scaffold render and check scripts.
- Added pilot values file for staged rendering.
- Validated raw templates and rendered scaffold.

## Phase 2: Harden Scaffold And Rollout Process

Status: complete

Todos:

- [x] Replace weak template placeholders with a stricter values contract.
- [x] Add `docs/rollout-checklist.md` for repo-by-repo rollout.
- [x] Add a sample rendered scaffold fixture for `misalud-lab-lis`.
- [x] Add script tests or fixture checks for `render_scaffold.py` and `check_scaffold.py`.
- [x] Confirm provider-neutral templates do not encode Claude-only behavior as policy.
- [x] Decide whether to commit the global project before pilot testing.

Exit criteria:

- Global scaffold validates from templates and from a rendered fixture.
- Rollout checklist is explicit enough to avoid accidental target repo edits.
- User approves moving to Phase 3.

## Phase 3: Scaffold-Test In `misalud-lab-lis`

Status: complete

Todos:

- [x] Confirm branch/worktree strategy.
- [x] Confirm exact copied files.
- [x] Render scaffold to a staging directory.
- [x] Copy only approved files into the pilot repo.
- [x] Compare old `CLAUDE.md` policy against rendered `AGENTS.md`.
- [x] Validate no safety rule was lost.
- [x] Validate no ignored/sensitive/generated paths are staged.
- [x] Stop before staging or committing unless separately approved.
- [x] Commit approved pilot scaffold files on `agent/provider-neutral-scaffold-test` as `65df16b`.

Exit criteria:

- Pilot repo has a provider-neutral scaffold on an approved branch/worktree.
- Claude and Codex adapter behavior is clear and minimal.
- Existing HIPAA/security/review safeguards are preserved.

## Phase 4: Add Bounded Agent-Facing Scripts

Status: complete

Todos:

- [x] Design provider-neutral `agent_status` behavior.
- [x] Design provider-neutral `agent_diff` behavior.
- [x] Design provider-neutral `agent_test` behavior.
- [x] Design provider-neutral `agent_policy_check` behavior.
- [x] Add templates or generators for those scripts.
- [x] Validate scripts never print sensitive file contents by default.

Exit criteria:

- Target repos can expose bounded status, diff, test, and policy checks to agents.
- Scripts are safe defaults and repo-customizable.

## Phase 5: Normalize Reusable Skills

Status: complete

Todos:

- [x] Harden review skill template.
- [x] Harden security skill template.
- [x] Harden database skill template.
- [x] Harden docs skill template.
- [x] Add guidance for provider-specific skill adapters where needed.
- [x] Validate skill templates cite canonical repo policies instead of duplicating them.

Exit criteria:

- Reusable skills are clear enough to scaffold into multiple repos without provider lock-in.

## Phase 6: Finalize Telemetry And Reporting

Status: complete

Todos:

- [x] Add telemetry fixture examples.
- [x] Add schema validation command.
- [x] Define provider field mappings for Claude and OpenAI/Codex where available.
- [x] Define aggregate metrics: cache hit ratio, cache write ratio, cost per task, cost per merged PR.
- [x] Confirm telemetry never stores prompts, raw diffs, logs, PHI, credentials, or customer data.

Exit criteria:

- Telemetry can ingest provider-specific data without making the policy layer provider-specific.

## Phase 7: Roll Out To The Next Repo

Status: ERP rollout staged, pending copy approval

Todos:

- [x] Select next repo: `misalud-lab-erp`.
- [x] Perform read-only audit.
- [x] Generate repo-specific values file.
- [x] Render scaffold to staging.
- [ ] Review with user before copying.
- [ ] Copy into approved branch/worktree.
- [ ] Validate and report.

Exit criteria:

- The process works repeatably beyond `misalud-lab-lis`.
