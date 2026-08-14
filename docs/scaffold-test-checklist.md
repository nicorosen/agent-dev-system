# Scaffold Test Checklist

Use this checklist before copying the global scaffold into a target repo.

## Preflight

- Confirm the target repo path.
- Confirm the current branch and dirty files.
- Confirm whether the test should happen in an isolated worktree or in place.
- Confirm the exact files that will be copied or modified.
- Confirm no target repo changes happen before approval.

## Copy Plan

Default scaffold copy:

- `templates/AGENTS.md` -> `AGENTS.md`
- `templates/agent/` -> `.agent/`
- `templates/CLAUDE.md` -> `CLAUDE.md` only during provider-adapter testing
- `templates/codex/` -> `.codex/` only during provider-adapter testing

Customize template variables from a read-only repo audit before copying.

Render into a staging directory first:

```bash
python3 scripts/render_scaffold.py --values <values.json> --out <staging-dir> --include-provider-adapters
python3 scripts/check_scaffold.py <staging-dir>
```

Inspect the staging directory before copying anything into the target repo.

## Validation

- Confirm only approved files changed.
- Confirm new scaffold files are not ignored by the target repo.
- Confirm sensitive and generated files remain ignored.
- Confirm provider adapters point to `AGENTS.md`.
- Confirm existing safety rules from prior provider files were preserved.
- Do not run paid review gates unless explicitly approved.

## Stop Conditions

Stop if:

- the target repo has unrelated uncommitted changes that overlap the scaffold files
- the target repo already has an `AGENTS.md` or `.agent/` with conflicting policy
- copying would weaken security, privacy, HIPAA, retention, review, or hook controls
- the rollout would add CI, remotes, deploy keys, mirrors, or repo-read automation
