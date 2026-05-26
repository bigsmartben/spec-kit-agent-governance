# Repository Governance Extension Governance

This document is the repository-level rule set for extending
`repository-governance`. It keeps extension changes aligned with Spec Kit's
extension model, the active repository governance contract, and this
repository's executable tests.

## Source Of Truth

- `extension.yml` declares extension metadata, command registration, hooks, tool requirements, and package discovery tags.
- `README.md` declares the user-facing contract, install flow, command entrypoint, scope, and verification command.
- `commands/speckit.repository-governance.refresh.md` declares the agent-facing command contract.
- `templates/repository-governance-template.md` declares the stable initial governance cache and generated section shape.
- `scripts/refresh_repository_governance.py` implements deterministic target resolution, evidence discovery, projection, and cleanup.
- `tests/test_governance_domains.py` is the executable contract for repository governance behavior and package boundaries.
- `CHANGELOG.md` records released and unreleased behavior changes.

## Extension Boundary

Extensions add new Spec Kit capabilities; presets override or compose existing Spec Kit workflow commands and templates. This repository is an extension, not a preset.

Use extension changes for repository governance refresh behavior, target file generation, integration metadata handling, active agent context projection, lifecycle hooks, and packaged runtime assets.

Do not add preset behavior here. Do not override core `/speckit.specify`, `/speckit.plan`, `/speckit.tasks`, `/speckit.implement`, or their templates. Do not add project implementation workflow ownership, external orchestration runners, or broad project-governance generation.

## Command, Template, And Script Ownership

- `commands/` owns the agent-facing command contract.
- `templates/` owns the stable generated governance shape.
- `scripts/` owns deterministic projection behavior.
- `tests/` owns executable expectations for all public behavior and protected boundaries.

Command files may name required inputs, outputs, procedure steps, helper commands, and final reporting requirements. They must not hide durable output structure that belongs in templates or scripts.

Template files define default governance wording, managed section structure, SSOT read order, vertical SSOT registry, write boundaries, MCP policy, skill contract, and handoff requirements. Keep templates concise, direct, self-contained, and free of project-specific examples.

Script files own behavior that must be repeatable without agent interpretation: resolving the active target, creating the internal cache, preserving user content, updating only managed sections, normalizing generated text to LF, removing stale managed sections, and reporting generated or updated status.

## Repository Governance Contract

- Output: active target file from Spec Kit integration metadata.
- Managed section: `SPECKIT GOVERNANCE`.
- Markers: `<!-- SPECKIT GOVERNANCE START -->` and `<!-- SPECKIT GOVERNANCE END -->`.
- Internal cache: `.specify/memory/repository-governance.md`.
- The active target file is the only review target.
- The internal cache is initialization evidence, not a separate user review artifact.
- Existing active managed section content is the refresh source when present.
- Content outside managed markers must be preserved.
- Stale managed sections in non-active known agent context files must be removed.

Do not generate implementation code, project architecture artifacts, feature specs, task plans, or broad repository rewrites from this extension.

## Target And Path Safety

Keep `CONTEXT_FILES` mappings explicit. Add new integrations only by mapping the integration key to its known agent context path.

Constrain target paths with `safe_project_path`. Reject empty, non-string, absolute, or traversal paths that do not resolve inside the project root.

Allowed writes are limited to:

- `.specify/memory/repository-governance.md`
- the resolved active target file
- managed section cleanup in known agent context files

Protected writes require an explicit user request and matching tests:

- implementation files
- secrets
- CI configuration
- permissions
- arbitrary repository paths
- MCP configuration
- tool settings

## Evidence And Directory Discovery

Repository evidence is descriptive. It must not override explicit SSOT content.

Capture vertical SSOT evidence for:

- Architecture
- Engineering
- Code Style
- Directory Structure
- Toolchain
- Agent Harness

Directory governance scans repository areas to depth 2. Include hidden, generated, cache, config, tool, and agent directories. Preserve the one-primary-purpose-per-directory rule and avoid injecting project-specific examples into generated governance.

When a vertical SSOT is missing or incomplete, infer temporary guidance only from current repository facts and keep that guidance subordinate to explicit SSOT content.

## Hooks And Runtime Requirements

Lifecycle hooks in `extension.yml` must call the namespaced command `speckit.repository-governance.refresh`.

Hook prompts must describe repository governance refresh behavior, not project implementation behavior. Optional hooks after constitution, plan, and tasks are acceptable when they keep the active governance target aligned.

Runtime requirements must stay explicit in `extension.yml`. This extension uses `uv` for the packaged helper invocation and local verification.

## Packaging Boundary

Package only runtime assets needed by `specify extension add`:

- `extension.yml`
- `commands/`
- `scripts/`
- `templates/`

Exclude development-only files through `.extensionignore`, including tests, local agent instructions, dependency locks, virtual environments, caches, and this governance document.

Build the local extension archive with:

```bash
rm -f dist/repository-governance.zip
mkdir -p dist
zip -qr dist/repository-governance.zip extension.yml commands scripts templates -x '*/__pycache__/*' '*.pyc'
```

Do not publish release archive URLs, bump versions, or change catalog metadata until release preparation.

## Change Discipline

Keep README, command, script, template, and tests aligned. A behavior change in one usually needs a targeted update in the others.

Update `CHANGELOG.md` under `## Unreleased` for behavior, packaging, command, template, or user contract changes.

Do not rename runtime files, command names, marker strings, cache paths, or target mapping keys without updating tests first.

Do not broaden write surfaces unless the user explicitly requests it and tests define the new boundary.

## Verification

After changing extension metadata, commands, scripts, templates, package boundaries, public docs, or this governance document, run:

```bash
uv run python -m py_compile scripts/refresh_repository_governance.py tests/test_governance_domains.py
uv run pytest -q
rm -f dist/repository-governance.zip
mkdir -p dist
zip -qr dist/repository-governance.zip extension.yml commands scripts templates -x '*/__pycache__/*' '*.pyc'
```

Run: `uv run pytest -q`.

Report:

- changed files
- commands run
- validation result
- unresolved risks
