# Repository Governance

## SSOT

- Metadata: `extension.yml`
- User contract: `README.md`
- Command contract: `commands/speckit.repository-governance.refresh.md`
- Projection: `scripts/refresh_repository_governance.py`
- Package builder: `tools/build_repository_governance_zip.py`
- Cache template: `templates/repository-governance-template.md`
- Extension governance: `docs/extension-governance.md`
- Tests: `tests/test_governance_domains.py`
- Change log: `CHANGELOG.md`

## Product

- Output: active agent platform project-governance projection from safe `context_file` override or Spec Kit integration metadata
- File mode: full generated projection file
- Cache: none
- Review target: active agent platform target only

## Scope

- Resolve and generate only the active agent platform target
- Overwrite existing active target with full project-governance projection
- Review and report only the active agent platform target
- Distill detected repository areas into action rules
- Capture repository facts as vertical SSOT evidence
- Repository area depth: 2
- Repository areas include hidden and cache directories
- Directory responsibility: one primary purpose per directory
- Clean legacy managed sections only from non-active context files enumerated by `CONTEXT_FILES`
- No implementation code generation
- No project implementation artifact generation

## Commands

```bash
uv run python -m py_compile scripts/refresh_repository_governance.py tools/build_repository_governance_zip.py tests/test_governance_domains.py
uv run pytest -q
uv run python tools/build_repository_governance_zip.py
```

## Rules

- Keep README, command, script, template, extension governance, changelog, and tests aligned.
- Keep generated project-governance projections concise, direct, and self-contained.
- Do not reintroduce managed markers; legacy managed sections are cleanup targets only.
- Keep target mappings explicit in `CONTEXT_FILES`.
- Constrain target paths with `safe_project_path`.
- Normalize generated text to LF.
- Exclude dev-only files through `.extensionignore`.
- Update `CHANGELOG.md` for behavior changes.
- Package only runtime assets required by Spec Kit extension install.

## Integration Boundary

- This repository owns the `repository-governance` extension source, tests,
  release artifact, and source documentation.
- Do not open pull requests from this repository directly to `github/spec-kit`.
- Do not push branches to `github/spec-kit` or add workflow automation that
  targets `github/spec-kit` for pull requests, repository dispatches, or direct
  writes.
- If a Spec Kit catalog or bundled snapshot update is needed, target the
  `bigsmartben/spec-kit` integration fork first. The integration fork owns any
  downstream pull request to `github/spec-kit`.
- Source releases must provide source-backed metadata for the integration fork:
  repository URL, release version, source commit SHA, download URL, and
  validation evidence.

## Boundaries

- Write surface:
  - resolved active agent platform target
  - legacy managed-section cleanup in non-active context files enumerated by `CONTEXT_FILES`
- Protected files: implementation paths, secrets, CI configuration, MCP configuration, permissions, tool settings, and arbitrary repository paths outside the resolved write surface.
- Protected-file writes require explicit user request, a named matching contract or regression test, and passing validation commands.
- Secrets: never log, never write.
- User edits: preserve.

## Handoff

- changed files
- commands run
- validation result
- unresolved risks
