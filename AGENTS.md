# Repository Governance

## SSOT

- Metadata: `extension.yml`
- User contract: `README.md`
- Command contract: `commands/speckit.repository-governance.refresh.md`
- Projection: `scripts/refresh_repository_governance.py`
- Cache template: `templates/repository-governance-template.md`
- Extension governance: `docs/extension-governance.md`
- Tests: `tests/test_governance_domains.py`
- Change log: `CHANGELOG.md`

## Product

- Output: active repository governance file from Spec Kit integration metadata
- Managed section: `SPECKIT GOVERNANCE`
- Cache: `.specify/memory/repository-governance.md`
- Cache status: internal
- Review target: active target file only

## Scope

- Generate missing target governance file
- Update existing target managed section
- Distill detected repository areas into action rules
- Capture repository facts as vertical SSOT evidence
- Repository area depth: 2
- Repository areas include hidden and cache directories
- Directory responsibility: one primary purpose per directory
- Preserve content outside managed markers
- Clean stale managed sections from non-active targets
- No implementation code generation
- No project-governance ownership

## Commands

```bash
uv run python -m py_compile scripts/refresh_repository_governance.py tests/test_governance_domains.py
uv run pytest -q
```

## Rules

- Keep README, command, script, template, extension governance, changelog, and tests aligned.
- Keep generated governance concise, direct, and self-contained.
- Preserve markers:
  - `<!-- SPECKIT GOVERNANCE START -->`
  - `<!-- SPECKIT GOVERNANCE END -->`
- Keep target mappings explicit in `CONTEXT_FILES`.
- Constrain target paths with `safe_project_path`.
- Normalize generated text to LF.
- Exclude dev-only files through `.extensionignore`.
- Update `CHANGELOG.md` for behavior changes.
- Package only runtime assets required by Spec Kit extension install.

## Boundaries

- Write surface: `.specify/memory/repository-governance.md` and managed sections in known agent context files.
- Protected files: implementation, secrets, CI, permissions, arbitrary repository paths.
- Protected-file writes: explicit user request plus matching tests.
- Secrets: never log, never write.
- User edits: preserve.

## Handoff

- changed files
- commands run
- validation result
- unresolved risks
