# Repository Governance Extension Governance

This document is the repository-level rule set for extending
`repository-governance`. It keeps extension changes aligned with Spec Kit's
extension model, the active project-governance projection contract, and this
repository's executable tests.

## Source Of Truth

- `extension.yml` declares extension metadata, command registration, hooks, tool requirements, and package discovery tags.
- `README.md` declares the user-facing contract, install flow, command entrypoint, scope, and verification command.
- `commands/speckit.repository-governance.refresh.md` declares the agent-facing command contract.
- `templates/repository-governance-template.md` declares the stable projection template and generated file shape.
- `scripts/refresh_repository_governance.py` implements deterministic target resolution, evidence discovery, project-governance projection, and cleanup.
- `tools/build_repository_governance_zip.py` implements deterministic runtime extension package creation.
- `tests/test_governance_domains.py` is the executable contract for project-governance projection behavior and package boundaries.
- `CHANGELOG.md` records released and unreleased behavior changes.

## Extension Boundary

Extensions add new Spec Kit capabilities; presets override or compose existing Spec Kit workflow commands and templates. This repository is an extension, not a preset.

Use extension changes for project-governance projection refresh behavior, target file generation, integration metadata handling, active agent platform projection, lifecycle hooks, and packaged runtime assets.

Do not add preset behavior here. Do not override core `/speckit.specify`, `/speckit.plan`, `/speckit.tasks`, `/speckit.implement`, or their templates. Do not add project implementation workflow ownership, external orchestration runners, or project implementation artifact generation.

## Command, Template, And Script Ownership

- `commands/` owns the agent-facing command contract.
- `templates/` owns the stable projection template and generated file shape.
- `scripts/` owns deterministic project-governance projection behavior.
- `tools/` owns development and release helper scripts that are excluded from runtime extension packages.
- `tests/` owns executable expectations for all public behavior and protected boundaries.

Command files may name required inputs, outputs, procedure steps, helper commands, and final reporting requirements. They must not hide durable output structure that belongs in templates or scripts.

Template files define default projection wording, file structure, authority order, vertical SSOT registry, repository workflow, write boundaries, agent adapter contract, scenario capability index, MCP policy, skill contract, and handoff requirements. Keep templates concise, direct, self-contained, and free of project-specific examples.

Script files own behavior that must be repeatable without agent interpretation: resolving the active agent platform target, scanning current repository evidence on every run, overwriting the active agent platform target, normalizing generated text to LF, projecting adapter-specific capability rules, cleaning legacy marker blocks from non-active targets, and reporting generated or updated status.

## Project-Governance Projection Contract

- Output: active agent platform target from safe `context_file` override or Spec Kit integration metadata.
- File mode: full generated projection file.
- Cache: none.
- The active agent platform target is the only review target.
- Existing active target content is overwritten on refresh.
- Stale legacy marker blocks in non-active context files enumerated by `CONTEXT_FILES` may be removed.
- Legacy `SPECKIT GOVERNANCE` sections are migration cleanup targets, not the long-term projection authority.

Do not generate implementation code, project architecture artifacts, feature specs, task plans, or broad repository rewrites from this extension.

## Target And Path Safety

Keep `CONTEXT_FILES` mappings explicit. Add new integrations only by mapping the integration key to its known agent context path.

Constrain mapped target paths with `safe_project_path`. Reject empty, non-string, absolute, or traversal paths that do not resolve inside the project root.

Custom `.specify/init-options.json` `context_file` targets must resolve through the context-file safety gate: relative path, inside the project root, Markdown/rules text suffix, and an agent/rules/instructions/governance filename. Do not accept protected implementation, CI, MCP, secrets, permissions, or arbitrary repository files as custom projection targets.

Allowed writes are limited to:

- the resolved active agent platform target
- legacy marker block cleanup in non-active context files enumerated by `CONTEXT_FILES`

Protected writes require an explicit user request, a named matching contract or regression test, and passing validation commands:

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
- Agent Harness

Repository fact detection should cover repository-level docs and policy files, Spec Kit metadata, extension assets, command/template governance contracts, source and test paths, feature specs, API contracts, build configuration, runtime/deployment configuration, package manifests, lockfiles, task runners, development commands from package scripts or Python/uv test conventions, and active agent harness evidence. Keep detection deterministic, bounded to explicit file/path families, and broad enough for extension repositories as well as application repositories.

Directory governance scans repository areas to depth 2. Include hidden, generated, cache, config, tool, and agent directories. Preserve the one-primary-purpose-per-directory rule and avoid injecting project-specific examples into generated projections.

When a vertical SSOT is missing or incomplete, infer temporary guidance only from current repository facts and keep that guidance subordinate to explicit SSOT content.

## Agent Adapter And Capability Index

The extension projects project-governance and repository capabilities through a Spec Kit Agent Adapter layer:

- Repository Capability abstracts repository-local skills and MCP evidence into scenario-level capabilities.
- Spec Kit Agent Adapter maps integration metadata to the active agent platform target and supported discovery behavior.
- Platform Projection emits only the rules the active agent platform target can safely apply.

Repository-local `SKILL.md` files are capability specs. The script may extract declared name, description, trigger, and source path to build a deterministic scenario index. The index must describe when to read the skill before planning or editing; it must not be a bare file-path inventory.

MCP configuration differs across agent platforms. Repository MCP config files are candidates and evidence unless the active adapter explicitly supports them. Generated governance must instruct agents to enumerate available runtime servers, resources, and tools before use, and it must not claim that a repository config file proves an active tool is available.

## Hooks And Runtime Requirements

Lifecycle hooks in `extension.yml` must call the namespaced command `speckit.repository-governance.refresh`.

Hook prompts must describe project-governance projection refresh behavior, not project implementation behavior. Optional hooks after constitution, plan, and tasks are acceptable when they keep the active agent platform target aligned.

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
uv run python tools/build_repository_governance_zip.py
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
uv run python -m py_compile scripts/refresh_repository_governance.py tools/build_repository_governance_zip.py tests/test_governance_domains.py
uv run pytest -q
uv run python tools/build_repository_governance_zip.py
```

Run: `uv run pytest -q`.

Report:

- changed files
- commands run
- validation result
- unresolved risks
