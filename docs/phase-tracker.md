# Agent Development System Phase Tracker

Use this as the persistent todo list for the provider-neutral agent development system.

## Phase Summary

- [x] Phase 0: Create control project and audit pilot repo
- [x] Phase 1: Build provider-neutral scaffold in global project
- [ ] Phase 2: Harden scaffold and rollout process
- [ ] Phase 3: Scaffold-test in `misalud-lab-lis`
- [ ] Phase 4: Add bounded agent-facing scripts
- [ ] Phase 5: Normalize reusable skills
- [ ] Phase 6: Finalize telemetry and reporting
- [ ] Phase 7: Roll out to the next repo

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

Status: complete, pending commit decision

Todos:

- [x] Replace weak template placeholders with a stricter values contract.
- [x] Add `docs/rollout-checklist.md` for repo-by-repo rollout.
- [x] Add a sample rendered scaffold fixture for `misalud-lab-lis`.
- [x] Add script tests or fixture checks for `render_scaffold.py` and `check_scaffold.py`.
- [x] Confirm provider-neutral templates do not encode Claude-only behavior as policy.
- [ ] Decide whether to commit the global project before pilot testing.

Exit criteria:

- Global scaffold validates from templates and from a rendered fixture.
- Rollout checklist is explicit enough to avoid accidental target repo edits.
- User approves moving to Phase 3.

## Phase 3: Scaffold-Test In `misalud-lab-lis`

Status: validated in isolated worktree, pending pilot commit decision

Todos:

- [x] Confirm branch/worktree strategy.
- [x] Confirm exact copied files.
- [x] Render scaffold to a staging directory.
- [x] Copy only approved files into the pilot repo.
- [x] Compare old `CLAUDE.md` policy against rendered `AGENTS.md`.
- [x] Validate no safety rule was lost.
- [x] Validate no ignored/sensitive/generated paths are staged.
- [ ] Stop before staging or committing unless separately approved.

Exit criteria:

- Pilot repo has a provider-neutral scaffold on an approved branch/worktree.
- Claude and Codex adapter behavior is clear and minimal.
- Existing HIPAA/security/review safeguards are preserved.

## Phase 4: Add Bounded Agent-Facing Scripts

Status: pending

Todos:

- [ ] Design provider-neutral `agent_status` behavior.
- [ ] Design provider-neutral `agent_diff` behavior.
- [ ] Design provider-neutral `agent_test` behavior.
- [ ] Design provider-neutral `agent_policy_check` behavior.
- [ ] Add templates or generators for those scripts.
- [ ] Validate scripts never print sensitive file contents by default.

Exit criteria:

- Target repos can expose bounded status, diff, test, and policy checks to agents.
- Scripts are safe defaults and repo-customizable.

## Phase 5: Normalize Reusable Skills

Status: pending

Todos:

- [ ] Harden review skill template.
- [ ] Harden security skill template.
- [ ] Harden database skill template.
- [ ] Harden docs skill template.
- [ ] Add guidance for provider-specific skill adapters where needed.
- [ ] Validate skill templates cite canonical repo policies instead of duplicating them.

Exit criteria:

- Reusable skills are clear enough to scaffold into multiple repos without provider lock-in.

## Phase 6: Finalize Telemetry And Reporting

Status: pending

Todos:

- [ ] Add telemetry fixture examples.
- [ ] Add schema validation command.
- [ ] Define provider field mappings for Claude and OpenAI/Codex where available.
- [ ] Define aggregate metrics: cache hit ratio, cache write ratio, cost per task, cost per merged PR.
- [ ] Confirm telemetry never stores prompts, raw diffs, logs, PHI, credentials, or customer data.

Exit criteria:

- Telemetry can ingest provider-specific data without making the policy layer provider-specific.

## Phase 7: Roll Out To The Next Repo

Status: pending pilot validation

Todos:

- [ ] Select next repo.
- [ ] Perform read-only audit.
- [ ] Generate repo-specific values file.
- [ ] Render scaffold to staging.
- [ ] Review with user before copying.
- [ ] Copy into approved branch/worktree.
- [ ] Validate and report.

Exit criteria:

- The process works repeatably beyond `misalud-lab-lis`.
