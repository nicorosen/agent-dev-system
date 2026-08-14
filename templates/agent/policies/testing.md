# Testing Policy

Use the smallest validation that proves the change, then broaden when the risk or blast radius requires it.

## Baseline Commands

{{BASELINE_COMMANDS}}

## Safety-Focused Tests

Run or consider these when touching security, audit, retention, config, auth, privacy, or sensitive-data surfaces:

- {{SAFETY_TESTS}}

## External And Hardware Tests

Do not run tests or scripts that write to external systems, production databases, printers, devices, or customer/patient records without explicit approval. If a test uses generated data, name the target environment and cleanup plan before running it.

## Documentation-Only Changes

For documentation-only policy changes, default validation is:

- check the created files exist
- check cross-references resolve
- check git status for unexpected changes
- do not run paid review gates unless the user asks

