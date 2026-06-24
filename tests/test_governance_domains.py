import importlib.util
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "templates" / "repository-governance-template.md"
SCRIPT = ROOT / "scripts" / "refresh_repository_governance.py"
BUILD_SCRIPT = ROOT / "tools" / "build_repository_governance_zip.py"
README = ROOT / "README.md"
AGENTS = ROOT / "AGENTS.md"
COMMAND = ROOT / "commands" / "speckit.repository-governance.refresh.md"
EXTENSION = ROOT / "extension.yml"
EXTENSION_IGNORE = ROOT / ".extensionignore"
EXTENSION_GOVERNANCE = ROOT / "docs" / "extension-governance.md"
GIT_IGNORE = ROOT / ".gitignore"
CI_WORKFLOW = ROOT / ".github" / "workflows" / "ci.yml"
ARTIFACT_WORKFLOW = ROOT / ".github" / "workflows" / "extension-artifact.yml"
BUILD_COMMAND = "uv run python tools/build_repository_governance_zip.py"
PY_COMPILE_COMMAND = "uv run --locked python -m py_compile scripts/refresh_repository_governance.py tools/build_repository_governance_zip.py tests/test_governance_domains.py"


def load_refresh_module():
    spec = importlib.util.spec_from_file_location("refresh_repository_governance", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def assert_repository_governance_framework(text: str) -> None:
    assert "Repository Governance Framework" in text
    assert "Vertical SSOT Registry" in text
    assert "Architecture SSOT" in text
    assert "Engineering SSOT" in text
    assert "Code Style SSOT" in text
    assert "Directory Structure SSOT" in text
    assert "Toolchain SSOT" in text
    assert "Agent Harness SSOT" in text
    assert "architecture methodology: owned by Architecture SSOT" in text
    assert "4+1" not in text


def assert_vertical_ssot_evidence(text: str) -> None:
    assert "## Vertical SSOT Evidence" in text
    assert "- Architecture evidence:" in text
    assert "- Engineering evidence:" in text
    assert "- Code Style evidence:" in text
    assert "- Directory Structure evidence:" in text
    assert "- Toolchain evidence:" in text
    assert "- Agent Harness evidence:" in text


def test_template_defines_repository_governance_framework_ssot():
    text = TEMPLATE.read_text(encoding="utf-8")

    assert_repository_governance_framework(text)


def test_template_declares_final_outputs_without_placeholders():
    text = TEMPLATE.read_text(encoding="utf-8")

    assert "## Final Output" in text
    assert "active repository governance file" in text
    assert "cache: internal" in text
    assert "TODO(" not in text
    final_outputs = text.split("## Final Output", 1)[1].split("## Scope", 1)[0]
    assert "- active repository governance file" in final_outputs
    assert "- cache: internal" in final_outputs


def test_template_protects_refresh_markers_and_scopes_broad_updates():
    text = TEMPLATE.read_text(encoding="utf-8")

    assert "`<!-- SPECKIT GOVERNANCE START -->`" in text
    assert "`<!-- SPECKIT GOVERNANCE END -->`" in text
    assert "## Agent Platform Adapter" in text
    assert "## Capability Index" in text
    assert "Repository Capability: abstract repository-local skill and MCP evidence into scenario capabilities." in text
    assert "Config candidates: evidence only, not proof of active tools." in text
    assert "Repository-local skill specs should declare" in text
    assert "Required fields: purpose" not in text
    assert "update only when in scope and authorized" in text
    assert "Change impact: update linked code" not in text


def test_readme_positions_extension_as_repository_governance_framework():
    text = README.read_text(encoding="utf-8")

    assert "Generate the active Repository Governance Framework SSOT section." in text
    assert "Active target file from Spec Kit integration metadata." in text
    assert "Project agent platform adapter rules from Spec Kit integration metadata." in text
    assert "Build a scenario capability index for repository-local skills and MCP-backed external tool evidence." in text
    assert "MCP config files are reported as candidates and evidence only" in text
    assert "Example:" not in text
    assert "Codex `AGENTS.md`" not in text
    assert "not a general-purpose `AGENTS.md` initializer" not in text


def test_extension_governance_defines_repository_extension_contract():
    assert EXTENSION_GOVERNANCE.is_file()
    text = EXTENSION_GOVERNANCE.read_text(encoding="utf-8")

    assert "Repository Governance Extension Governance" in text
    assert "`extension.yml` declares extension metadata, command registration, hooks, tool requirements, and package discovery tags." in text
    assert "Extensions add new Spec Kit capabilities; presets override or compose existing Spec Kit workflow commands and templates." in text
    assert "This repository is an extension, not a preset." in text
    assert "`commands/` owns the agent-facing command contract." in text
    assert "`templates/` owns the stable generated governance shape." in text
    assert "`scripts/` owns deterministic projection behavior." in text
    assert "The extension projects repository capabilities through a Spec Kit Agent Adapter layer:" in text
    assert "MCP configuration differs across agent platforms." in text
    assert "The active target file is the only review target." in text
    assert "Keep `CONTEXT_FILES` mappings explicit." in text
    assert "Constrain target paths with `safe_project_path`." in text
    assert "Run: `uv run pytest -q`." in text


def test_build_command_documents_runtime_extension_package():
    readme = README.read_text(encoding="utf-8")
    agents = AGENTS.read_text(encoding="utf-8")
    governance = EXTENSION_GOVERNANCE.read_text(encoding="utf-8")
    extension_ignore = set(EXTENSION_IGNORE.read_text(encoding="utf-8").splitlines())
    git_ignore = set(GIT_IGNORE.read_text(encoding="utf-8").splitlines())

    assert "## Build" in readme
    assert "Build the local extension archive with:" in governance
    assert BUILD_COMMAND in readme
    assert BUILD_COMMAND in agents
    assert BUILD_COMMAND in governance
    assert "dist/" in extension_ignore
    assert "*.zip" in extension_ignore
    assert "tools/" in extension_ignore
    assert "dist/" in git_ignore
    assert "*.zip" in git_ignore


def test_build_script_creates_runtime_extension_package(tmp_path):
    output = tmp_path / "repository-governance.zip"

    result = subprocess.run(
        [sys.executable, str(BUILD_SCRIPT), "--output", str(output)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert output.as_posix() in result.stdout
    with zipfile.ZipFile(output) as archive:
        names = set(archive.namelist())

    assert names == {
        "extension.yml",
        "commands/speckit.repository-governance.refresh.md",
        "scripts/refresh_repository_governance.py",
        "templates/repository-governance-template.md",
    }
    assert "tools/build_repository_governance_zip.py" not in names
    assert "tests/test_governance_domains.py" not in names
    assert "docs/extension-governance.md" not in names
    assert "AGENTS.md" not in names


def test_ci_workflow_runs_governance_contract_on_supported_python_versions():
    text = CI_WORKFLOW.read_text(encoding="utf-8")

    assert "name: Governance Contract" in text
    assert "permissions:" in text
    assert "contents: read" in text
    assert "pull_request:" in text
    assert 'branches: ["main"]' in text
    assert "workflow_dispatch:" in text
    assert "cancel-in-progress: true" in text
    assert 'python-version: ["3.10", "3.13"]' in text
    assert "astral-sh/setup-uv@" in text
    assert PY_COMPILE_COMMAND in text
    assert "uv run --locked pytest -q" in text


def test_extension_artifact_workflow_builds_runtime_zip_and_can_open_spec_kit_pr():
    text = ARTIFACT_WORKFLOW.read_text(encoding="utf-8")

    assert "name: Extension Artifact" in text
    assert "contents: write" in text
    assert 'tags: ["v*"]' in text
    assert "workflow_dispatch:" in text
    assert "create_integration_pr:" in text
    assert "SPEC_KIT_FORK_PR_TOKEN" in text
    assert "bigsmartben/spec-kit" in text
    assert "extensions/repository-governance" in text
    assert "extension-release-v${VERSION}" in text
    assert "gh pr create --repo bigsmartben/spec-kit" in text
    assert PY_COMPILE_COMMAND in text
    assert "uv run --locked pytest -q" in text
    assert "Check workflow YAML syntax" in text
    assert "python - <<'PY'" in text
    assert "yaml.safe_load" in text
    assert "repository-governance-v${VERSION}.zip" in text
    assert 'python3 tools/build_repository_governance_zip.py --output "${ZIP_NAME}"' in text
    assert "required_entries" in text
    assert '"extension.yml"' in text
    assert '"commands/speckit.repository-governance.refresh.md"' in text
    assert '"scripts/refresh_repository_governance.py"' in text
    assert '"templates/repository-governance-template.md"' in text
    assert 'forbidden_prefixes = (".github/", ".git/", "docs/", "tests/", "tools/", "__pycache__/")' in text
    assert 'forbidden_entries = {"AGENTS.md", "pyproject.toml", "uv.lock", "CHANGELOG.md", ".extensionignore"}' in text
    assert "Smoke install extension on GitHub runner" in text
    assert "specify init --here --integration codex --script sh --ignore-agent-tools" in text
    assert 'specify extension remove repository-governance --force' in text
    assert 'specify extension add --dev "$GITHUB_WORKSPACE"' in text


def test_workflow_files_are_valid_yaml():
    yaml = pytest.importorskip("yaml")

    for workflow in (CI_WORKFLOW, ARTIFACT_WORKFLOW):
        assert yaml.safe_load(workflow.read_text(encoding="utf-8"))


def test_usage_is_single_command_generate_or_update_flow():
    readme = README.read_text(encoding="utf-8")
    command = COMMAND.read_text(encoding="utf-8")

    assert "Generate missing target governance file." in readme
    assert "Update existing target governance file." in readme
    assert "review and edit the memory file" not in readme
    assert "run the refresh command again" not in readme
    assert "Review only the active target file." in readme
    assert "Preserve managed markers verbatim." in readme
    assert "Use existing managed section as refresh source." in command
    assert "Preserve managed markers verbatim." in command
    assert "generated or updated" in command
    assert "inserted or replaced" not in command


def test_write_projection_reports_generated_or_updated(tmp_path):
    module = load_refresh_module()
    target = tmp_path / "AGENTS.md"

    generated = module.write_projection(target, "new governance")
    target.write_text("existing governance", encoding="utf-8")
    updated = module.write_projection(target, "updated governance")

    assert generated == "generated"
    assert updated == "updated"


def test_cli_report_prioritizes_active_target_and_labels_cache_internal(tmp_path):
    extension_root = tmp_path / ".specify" / "extensions" / "repository-governance"
    (extension_root / "scripts").mkdir(parents=True)
    (extension_root / "templates").mkdir(parents=True)
    shutil.copy2(SCRIPT, extension_root / "scripts" / "refresh_repository_governance.py")
    shutil.copy2(TEMPLATE, extension_root / "templates" / "repository-governance-template.md")
    (tmp_path / ".specify" / "integration.json").write_text(
        '{"default_integration":"codex","installed_integrations":["codex"]}',
        encoding="utf-8",
    )

    result = subprocess.run(
        [sys.executable, ".specify/extensions/repository-governance/scripts/refresh_repository_governance.py"],
        cwd=tmp_path,
        text=True,
        capture_output=True,
        check=False,
    )
    lines = result.stdout.splitlines()

    assert result.returncode == 0, result.stderr
    assert lines[0] == "Target governance file: AGENTS.md"
    assert lines[1] == "Governance file: generated"
    assert "Review target: AGENTS.md" in lines
    assert any(line.startswith("Internal initialization cache: ") for line in lines)
    assert not any(line.startswith("Source memory: ") for line in lines)
    assert not any(line.startswith("Memory: ") for line in lines)


def test_write_projection_preserves_user_authored_content(tmp_path):
    module = load_refresh_module()
    target = tmp_path / "AGENTS.md"
    target.write_text(
        "\n".join(
            [
                "# Project Instructions",
                "",
                "Keep this user-authored introduction.",
                "",
                module.MARKER_START,
                "old generated content",
                module.MARKER_END,
                "",
                "Keep this user-authored footer.",
            ]
        ),
        encoding="utf-8",
    )

    action = module.write_projection(
        target,
        "\n".join([module.MARKER_START, "new generated content", module.MARKER_END, ""]),
    )
    text = target.read_text(encoding="utf-8")

    assert action == "updated"
    assert "Keep this user-authored introduction." in text
    assert "Keep this user-authored footer." in text
    assert "new generated content" in text
    assert "old generated content" not in text


def test_remove_stale_sections_when_active_target_changes(tmp_path):
    module = load_refresh_module()
    old_target = tmp_path / "AGENTS.md"
    active_target = tmp_path / "CLAUDE.md"
    old_target.write_text(
        "\n".join(
            [
                "# Existing Codex Context",
                "",
                "User content stays.",
                "",
                module.MARKER_START,
                "stale generated content",
                module.MARKER_END,
                "",
            ]
        ),
        encoding="utf-8",
    )
    active_target.write_text("# Claude Context\n", encoding="utf-8")

    module.remove_stale_sections(
        tmp_path,
        active_target,
        {},
        {"default_integration": "claude", "installed_integrations": ["codex", "claude"]},
    )
    old_text = old_target.read_text(encoding="utf-8")

    assert "User content stays." in old_text
    assert module.MARKER_START not in old_text
    assert "stale generated content" not in old_text


def test_resolve_target_uses_spec_kit_integration_metadata(tmp_path):
    module = load_refresh_module()

    assert module.resolve_target(tmp_path, {"default_integration": "codex"}, {}) == tmp_path / "AGENTS.md"
    assert module.resolve_target(tmp_path, {"default_integration": "claude"}, {}) == tmp_path / "CLAUDE.md"
    assert module.resolve_target(tmp_path, {"default_integration": "cursor-agent"}, {}) == tmp_path / ".cursor/rules/specify-rules.mdc"
    assert module.resolve_target(
        tmp_path,
        {"default_integration": "codex"},
        {"context_file": "custom/AGENT_RULES.md"},
    ) == tmp_path / "custom/AGENT_RULES.md"


def test_projection_defines_repository_governance_framework_ssot(tmp_path):
    module = load_refresh_module()
    root = tmp_path
    memory = root / ".specify" / "memory"
    memory.mkdir(parents=True)
    (memory / "repository-governance.md").write_text(TEMPLATE.read_text(encoding="utf-8"), encoding="utf-8")

    projection = module.render_projection(root, root / "AGENTS.md", {"default_integration": "codex"}, False)

    assert_repository_governance_framework(projection)
    assert_vertical_ssot_evidence(projection)
    assert "Constitution" not in projection
    assert "## Repository Governance" in projection
    assert "- SSOT: this managed section." in projection
    assert "Repository governance SSOT: `.specify/memory/repository-governance.md`" not in projection
    assert "`.specify/memory/repository-governance.md` is the SSOT" not in projection
    assert "Generated Governance Boundaries" not in projection
    assert "agent-governance refresh command may create" not in projection
    assert "This generated section" not in projection
    assert "Initialization Evidence Cache:" not in projection
    assert "## Governance Domains" not in projection
    assert "## Resolved Repository Context" not in projection


def test_projection_includes_repository_evidence_and_development_commands(tmp_path):
    module = load_refresh_module()
    root = tmp_path
    memory = root / ".specify" / "memory"
    memory.mkdir(parents=True)
    (memory / "repository-governance.md").write_text(
        "\n".join(
            [
                "# Repository Governance",
                "",
                "## Repository Evidence",
                "",
                "- README: `README.md`",
                "- Source paths: `src/`",
                "- Test paths: `tests/`",
                "",
                "## Vertical SSOT Evidence",
                "",
                "- Architecture evidence: `src/`",
                "- Engineering evidence: `package.json`",
                "- Code Style evidence: `eslint.config.js`",
                "- Directory Structure evidence: `src/`",
                "- Toolchain evidence: `package.json`",
                "- Agent Harness evidence: `AGENTS.md`",
                "",
                "## Development Commands",
                "",
                "- `npm test` -> `vitest run`",
                "- manifest commands over ad hoc equivalents",
                "",
                "## Write Boundaries",
                "",
                "- Preserve user-authored content outside managed markers.",
            ]
        ),
        encoding="utf-8",
    )

    projection = module.render_projection(root, root / "AGENTS.md", {"default_integration": "codex"}, False)

    assert "## Repository Evidence" in projection
    assert "- README: `README.md`" in projection
    assert "- Source paths: `src/`" in projection
    assert "## Vertical SSOT Evidence" in projection
    assert "- Architecture evidence: `src/`" in projection
    assert "## Development Commands" in projection
    assert "- `npm test` -> `vitest run`" in projection


def test_repository_areas_scan_two_directory_levels_including_hidden_and_cache_dirs(tmp_path):
    module = load_refresh_module()
    root = tmp_path
    for path in (
        "docs/reference",
        "src/pipeline/deep/ignored",
        "tests/browser",
        "node_modules/package",
        ".git/hooks",
    ):
        (root / path).mkdir(parents=True)
    (root / ".specify" / "extensions" / "repository-governance" / "templates").mkdir(parents=True)
    (root / ".specify" / "extensions" / "repository-governance" / "templates" / "repository-governance-template.md").write_text(
        TEMPLATE.read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    (root / ".specify" / "integration.json").write_text('{"default_integration": "codex"}', encoding="utf-8")

    module.ensure_memory(root)
    projection = module.render_projection(root, root / "AGENTS.md", {"default_integration": "codex"}, True)
    areas = projection.split("## Repository Areas", 1)[1].split("## Development Commands", 1)[0]

    assert "## Repository Areas" in projection
    assert "- `docs/`: review before changing linked areas." in areas
    assert "- `docs/reference/`: change with parent area `docs/`." in areas
    assert "- `src/`: review before changing linked areas." in areas
    assert "- `src/pipeline/`: change with parent area `src/`." in areas
    assert "- `tests/`: review before changing linked areas." in areas
    assert "- `tests/browser/`: change with parent area `tests/`." in areas
    assert "- `.git/`: review before changing linked areas." in areas
    assert "- `.git/hooks/`: change with parent area `.git/`." in areas
    assert "- `.specify/`: review before changing linked areas." in areas
    assert "- `.specify/extensions/`: change with parent area `.specify/`." in areas
    assert "- `.specify/memory/`: change with parent area `.specify/`." in areas
    assert "- `node_modules/`: review before changing linked areas." in areas
    assert "- `node_modules/package/`: change with parent area `node_modules/`." in areas
    assert "src/pipeline/deep" not in areas
    assert "math-animation" not in areas
    assert "renderer" not in areas


def test_projection_includes_generic_directory_governance(tmp_path):
    module = load_refresh_module()
    root = tmp_path
    memory = root / ".specify" / "memory"
    memory.mkdir(parents=True)
    (memory / "repository-governance.md").write_text(TEMPLATE.read_text(encoding="utf-8"), encoding="utf-8")

    projection = module.render_projection(root, root / "AGENTS.md", {"default_integration": "codex"}, False)
    directory_governance = projection.split("## Directory Governance", 1)[1].split("## Development Commands", 1)[0]

    assert "## Directory Governance" in projection
    assert "- Responsibility: one primary purpose per directory." in projection
    assert "- Depth: 2." in projection
    assert "- Coverage: include visible, hidden, generated, cache, config/env, tool, and agent directories." in projection
    assert "- Mixed concerns: follow existing repo convention or split responsibility." in projection
    assert "- Change impact: review linked code, tests, docs, config/env, data, assets, generated files, and tool outputs; update only when in scope and authorized." in projection
    assert "Top level: responsibility domain" not in directory_governance
    assert "Level 2: parent-scoped subdomain" not in directory_governance
    assert "source, tests, docs" not in directory_governance
    assert "- Depth: 2." in projection
    assert "Codex" not in projection
    assert "Unity" not in projection


def test_projection_includes_agent_adapter_and_capability_index(tmp_path):
    module = load_refresh_module()
    root = tmp_path
    memory = root / ".specify" / "memory"
    memory.mkdir(parents=True)
    (memory / "repository-governance.md").write_text(TEMPLATE.read_text(encoding="utf-8"), encoding="utf-8")
    skill_dir = root / ".codex" / "skills" / "review"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(
        "\n".join(
            [
                "---",
                "name: code-review",
                "description: Review pull requests for behavioral regressions and missing tests.",
                "---",
                "",
                "# Code Review",
            ]
        ),
        encoding="utf-8",
    )
    (root / ".mcp.json").write_text('{"mcpServers":{"github":{"command":"github-mcp-server"}}}', encoding="utf-8")
    (root / "docs").mkdir()
    (root / "docs" / "mcp-notes.md").write_text("notes about mcp usage", encoding="utf-8")

    projection = module.render_projection(root, root / "AGENTS.md", {"default_integration": "codex"}, False)

    assert "## Agent Platform Adapter" in projection
    assert "- Active integration: codex" in projection
    assert "- Context target: AGENTS.md" in projection
    assert "- Skill discovery: repository-local `SKILL.md` capability specs, sorted by path." in projection
    assert "- MCP discovery: platform runtime enumeration first; repository config candidates are evidence only unless supported by this adapter." in projection
    assert "## Capability Index" in projection
    assert "- Repository capability: code-review" in projection
    assert "Scenario: Review pull requests for behavioral regressions and missing tests." in projection
    assert "Source: `.codex/skills/review/SKILL.md`." in projection
    assert "- Repository capability: MCP-backed external tools" in projection
    assert "Sources: MCP config candidates are evidence, not proof of active tools: `.mcp.json`." in projection
    assert "Runtime action: enumerate available servers, resources, and tools before use." in projection
    assert "docs/mcp-notes.md" not in projection


def test_unknown_agent_adapter_does_not_claim_mcp_config_support(tmp_path):
    module = load_refresh_module()
    root = tmp_path
    memory = root / ".specify" / "memory"
    memory.mkdir(parents=True)
    (memory / "repository-governance.md").write_text(TEMPLATE.read_text(encoding="utf-8"), encoding="utf-8")
    (root / "mcp.config.json").write_text("{}", encoding="utf-8")

    projection = module.render_projection(root, root / "AGENTS.md", {"default_integration": "unknown-agent"}, False)

    assert "- Active integration: unknown-agent" in projection
    assert "- Skill discovery: evidence-only repository scan; platform activation is integration-specific." in projection
    assert "- MCP discovery: platform-specific; repository config candidates are evidence only." in projection
    assert "Sources: MCP config candidates are evidence, not proof of active tools: `mcp.config.json`." in projection
    assert "MCP config supports active tools" not in projection


def test_scan_mcp_configs_only_returns_known_config_candidates(tmp_path):
    module = load_refresh_module()
    root = tmp_path
    (root / ".mcp.json").write_text("{}", encoding="utf-8")
    (root / "docs").mkdir()
    (root / "docs" / "mcp-notes.md").write_text("notes", encoding="utf-8")
    (root / "tool.mcp.backup").write_text("backup", encoding="utf-8")

    assert module.scan_mcp_configs(root) == [".mcp.json"]


def test_skill_capabilities_are_sorted_by_path(tmp_path):
    module = load_refresh_module()
    root = tmp_path
    for path, name, description in [
        ("z/skills/later/SKILL.md", "later-skill", "Use later."),
        ("a/skills/first/SKILL.md", "first-skill", "Use first."),
    ]:
        skill_path = root / path
        skill_path.parent.mkdir(parents=True, exist_ok=True)
        skill_path.write_text(
            "\n".join(["---", f"name: {name}", f"description: {description}", "---"]),
            encoding="utf-8",
        )

    lines = module.skill_capability_lines(root)
    first_index = lines.index("- Repository capability: first-skill")
    later_index = lines.index("- Repository capability: later-skill")

    assert first_index < later_index


def test_existing_generated_section_is_refresh_source_of_truth(tmp_path):
    module = load_refresh_module()
    root = tmp_path
    memory = root / ".specify" / "memory"
    memory.mkdir(parents=True)
    (memory / "repository-governance.md").write_text(
        "\n".join(
            [
                "# Repository Governance Source",
                "",
                "## Write Boundaries",
                "",
                "- Stale memory write boundary.",
                "",
                "## MCP Policy",
                "",
                "- Stale memory MCP policy.",
            ]
        ),
        encoding="utf-8",
    )
    target = root / "AGENTS.md"
    target.write_text(
        "\n".join(
            [
                module.MARKER_START,
                "## Repository Governance",
                "",
                "## Write Boundaries",
                "- Reviewed active write boundary.",
                "",
                "## MCP And External Tool Policy",
                "- Reviewed active MCP policy.",
                module.MARKER_END,
                "",
            ]
        ),
        encoding="utf-8",
    )

    projection = module.render_projection(root, target, {"default_integration": "codex"}, False)

    assert "- Reviewed active write boundary." in projection
    assert "- Reviewed active MCP policy." in projection
    assert "- Stale memory write boundary." not in projection
    assert "- Stale memory MCP policy." not in projection


def test_projection_authority_order_uses_active_generated_section_not_memory(tmp_path):
    module = load_refresh_module()
    root = tmp_path
    memory = root / ".specify" / "memory"
    memory.mkdir(parents=True)
    (memory / "repository-governance.md").write_text(TEMPLATE.read_text(encoding="utf-8"), encoding="utf-8")

    projection = module.render_projection(root, root / "AGENTS.md", {"default_integration": "codex"}, False)

    assert "2. Safety and permission constraints" in projection
    assert "3. Active `SPECKIT GOVERNANCE` section" in projection
    assert "Repository governance rules from `.specify/memory/repository-governance.md`" not in projection


def test_default_governance_does_not_inject_project_implementation_gate(tmp_path):
    module = load_refresh_module()
    root = tmp_path
    memory = root / ".specify" / "memory"
    memory.mkdir(parents=True)
    (memory / "repository-governance.md").write_text(TEMPLATE.read_text(encoding="utf-8"), encoding="utf-8")

    template = TEMPLATE.read_text(encoding="utf-8")
    projection = module.render_projection(root, root / "AGENTS.md", {"default_integration": "codex"}, False)
    combined = template + "\n" + projection

    assert "required project-governance artifacts" not in combined
    assert "owning project-governance workflow" not in combined
    assert "Non-Negotiable Execution Gates" not in combined
    assert "/speckit.implement" not in combined


def test_usage_is_spec_kit_uv_based():
    readme = README.read_text(encoding="utf-8")
    command = COMMAND.read_text(encoding="utf-8")
    extension = EXTENSION.read_text(encoding="utf-8")

    assert "uv run python" in readme
    assert "uv run python" in command
    assert 'name: "uv"' in extension
    assert "required: true" in extension
    assert "If Python is not available" not in command
    assert 'name: "python3"' not in extension


def test_extension_package_boundary_excludes_development_only_files():
    ignore = set(EXTENSION_IGNORE.read_text(encoding="utf-8").splitlines())

    assert "AGENTS.md" in ignore
    assert "docs/" in ignore
    assert "pyproject.toml" in ignore
    assert "uv.lock" in ignore
    assert "tests/" in ignore

    assert "extension.yml" not in ignore
    assert "commands/" not in ignore
    assert "scripts/" not in ignore
    assert "templates/" not in ignore


def test_extension_references_existing_runtime_files():
    extension = EXTENSION.read_text(encoding="utf-8")
    command = COMMAND.read_text(encoding="utf-8")

    assert 'file: "commands/speckit.repository-governance.refresh.md"' in extension
    assert (ROOT / "commands" / "speckit.repository-governance.refresh.md").is_file()
    assert ".specify/extensions/repository-governance/scripts/refresh_repository_governance.py" in command
    assert (ROOT / "scripts" / "refresh_repository_governance.py").is_file()
    assert (ROOT / "templates" / "repository-governance-template.md").is_file()


def test_packaged_runtime_generates_codex_governance_file(tmp_path):
    extension_root = tmp_path / ".specify" / "extensions" / "repository-governance"
    (extension_root / "scripts").mkdir(parents=True)
    (extension_root / "templates").mkdir(parents=True)
    shutil.copy2(SCRIPT, extension_root / "scripts" / "refresh_repository_governance.py")
    shutil.copy2(TEMPLATE, extension_root / "templates" / "repository-governance-template.md")
    (tmp_path / ".specify" / "integration.json").write_text(
        '{"default_integration":"codex","installed_integrations":["codex"]}',
        encoding="utf-8",
    )
    (tmp_path / "README.md").write_text("# Demo\n", encoding="utf-8")
    (tmp_path / "package.json").write_text(
        '{"scripts":{"test":"vitest run","lint":"eslint ."}}',
        encoding="utf-8",
    )
    (tmp_path / "src").mkdir()
    (tmp_path / "tests").mkdir()

    result = subprocess.run(
        [sys.executable, ".specify/extensions/repository-governance/scripts/refresh_repository_governance.py"],
        cwd=tmp_path,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "Target governance file: AGENTS.md" in result.stdout
    assert "Governance file: generated" in result.stdout
    generated = (tmp_path / "AGENTS.md").read_text(encoding="utf-8")
    assert "## Repository Evidence" in generated
    assert "- README: `README.md`" in generated
    assert_vertical_ssot_evidence(generated)
    assert "## Development Commands" in generated
    assert "- `npm test` -> `vitest run`" in generated


def test_vertical_ssot_evidence_extracts_repository_facts(tmp_path):
    module = load_refresh_module()
    root = tmp_path
    (root / ".specify" / "extensions" / "repository-governance" / "templates").mkdir(parents=True)
    (root / ".specify" / "extensions" / "repository-governance" / "templates" / "repository-governance-template.md").write_text(
        TEMPLATE.read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    (root / ".specify" / "integration.json").write_text('{"default_integration": "codex"}', encoding="utf-8")
    (root / ".github" / "workflows").mkdir(parents=True)
    (root / ".github" / "workflows" / "ci.yml").write_text("name: CI\n", encoding="utf-8")
    (root / "src" / "api").mkdir(parents=True)
    (root / "src" / "api" / "routes.py").write_text("@app.route('/health')\ndef health():\n    return 'ok'\n", encoding="utf-8")
    (root / "tests").mkdir()
    (root / "package.json").write_text('{"scripts": {"test": "vitest run"}}', encoding="utf-8")
    (root / "eslint.config.js").write_text("export default [];\n", encoding="utf-8")
    (root / "Dockerfile").write_text("FROM python:3.12\n", encoding="utf-8")
    (root / ".mcp.json").write_text("{}", encoding="utf-8")
    (root / "AGENTS.md").write_text("# Agent rules\n", encoding="utf-8")

    created = module.ensure_memory(root)
    text = (root / ".specify" / "memory" / "repository-governance.md").read_text(encoding="utf-8")

    assert created is True
    assert_vertical_ssot_evidence(text)
    assert "- Architecture evidence: `src/`, `src/api/routes.py`" in text
    assert "- Engineering evidence: `.github/workflows/ci.yml`, `package.json`" in text
    assert "- Code Style evidence: `eslint.config.js`, `tests/`" in text
    assert "- Directory Structure evidence:" in text
    assert "`src/`" in text
    assert "`tests/`" in text
    assert "- Toolchain evidence: `package.json`, `Dockerfile`" in text
    assert "- Agent Harness evidence: `AGENTS.md`, `.specify/integration.json`, `.mcp.json`" in text


def test_repository_evidence_captures_broader_repo_facts(tmp_path):
    module = load_refresh_module()
    root = tmp_path
    (root / ".specify" / "extensions" / "repository-governance" / "templates").mkdir(parents=True)
    (root / ".specify" / "extensions" / "repository-governance" / "templates" / "repository-governance-template.md").write_text(
        TEMPLATE.read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    (root / ".specify" / "integration.json").write_text('{"default_integration": "codex"}', encoding="utf-8")
    (root / "docs").mkdir()
    (root / "infra").mkdir()
    (root / "src").mkdir()
    (root / "e2e").mkdir()
    (root / "README.md").write_text("# Demo\n", encoding="utf-8")
    (root / "requirements-dev.txt").write_text("pytest\n", encoding="utf-8")
    (root / "pnpm-lock.yaml").write_text("lockfileVersion: '9.0'\n", encoding="utf-8")
    (root / "justfile").write_text("test:\n  pytest\n", encoding="utf-8")
    (root / "openapi.yaml").write_text("openapi: 3.0.0\n", encoding="utf-8")
    (root / "tsconfig.build.json").write_text("{}", encoding="utf-8")
    (root / "vite.config.ts").write_text("export default {}\n", encoding="utf-8")
    (root / ".env.example").write_text("APP_ENV=dev\n", encoding="utf-8")
    (root / "compose.yaml").write_text("services: {}\n", encoding="utf-8")
    (root / "AGENTS.md").write_text("# Agent rules\n", encoding="utf-8")

    created = module.ensure_memory(root)
    text = (root / ".specify" / "memory" / "repository-governance.md").read_text(encoding="utf-8")

    assert created is True
    assert "- Project docs: `docs/`" in text
    assert "- Spec Kit metadata: `.specify/integration.json`" in text
    assert "- Package manifest: `requirements-dev.txt`" in text
    assert "- Lockfiles: `pnpm-lock.yaml`" in text
    assert "- Task runners: `justfile`" in text
    assert "- Test paths: `e2e/`" in text
    assert "- API contracts: `openapi.yaml`" in text
    assert "- Build config: `vite.config.ts`, `tsconfig.build.json`" in text
    assert "- Runtime config: `.env.example`, `compose.yaml`, `infra/`" in text
    assert "- Toolchain evidence: `requirements-dev.txt`, `pnpm-lock.yaml`, `justfile`, `vite.config.ts`, `tsconfig.build.json`, `.env.example`, `compose.yaml`, `infra/`" in text


def test_extension_source_facts_and_python_uv_commands_are_detected(tmp_path):
    module = load_refresh_module()
    root = tmp_path
    (root / ".specify" / "extensions" / "repository-governance" / "templates").mkdir(parents=True)
    (root / ".specify" / "extensions" / "repository-governance" / "templates" / "repository-governance-template.md").write_text(
        TEMPLATE.read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    (root / ".specify" / "integration.json").write_text('{"default_integration": "codex"}', encoding="utf-8")
    (root / "commands").mkdir()
    (root / "scripts").mkdir()
    (root / "templates").mkdir()
    (root / "docs").mkdir()
    (root / "tests").mkdir()
    (root / "commands" / "speckit.repository-governance.refresh.md").write_text("# Command\n", encoding="utf-8")
    (root / "templates" / "repository-governance-template.md").write_text("# Template\n", encoding="utf-8")
    (root / "docs" / "extension-governance.md").write_text("# Governance\n", encoding="utf-8")
    (root / "extension.yml").write_text("extension:\n  id: repository-governance\n", encoding="utf-8")
    (root / ".extensionignore").write_text("tests/\n", encoding="utf-8")
    (root / "pyproject.toml").write_text("[project]\nname = \"demo\"\n", encoding="utf-8")
    (root / "uv.lock").write_text("version = 1\n", encoding="utf-8")
    (root / "AGENTS.md").write_text("# Agent rules\n", encoding="utf-8")

    created = module.ensure_memory(root)
    text = (root / ".specify" / "memory" / "repository-governance.md").read_text(encoding="utf-8")

    assert created is True
    assert "- Extension assets: `extension.yml`, `.extensionignore`, `commands/`, `templates/`" in text
    assert "- Source paths: `scripts/`, `commands/`, `templates/`" in text
    assert "- Architecture evidence: `scripts/`, `commands/`, `templates/`" in text
    assert "- Engineering evidence: `commands/speckit.repository-governance.refresh.md`, `templates/repository-governance-template.md`, `docs/extension-governance.md`, `pyproject.toml`" in text
    assert "- Toolchain evidence: `pyproject.toml`, `uv.lock`, `extension.yml`, `.extensionignore`, `commands/`, `templates/`" in text
    assert "- `uv run --locked pytest -q` -> pytest suite" in text


def test_feature_specs_are_reported_with_file_status(tmp_path):
    module = load_refresh_module()
    root = tmp_path
    (root / ".specify" / "extensions" / "repository-governance" / "templates").mkdir(parents=True)
    (root / ".specify" / "extensions" / "repository-governance" / "templates" / "repository-governance-template.md").write_text(
        TEMPLATE.read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    (root / ".specify" / "integration.json").write_text('{"default_integration": "codex"}', encoding="utf-8")
    feature = root / "specs" / "001-demo"
    feature.mkdir(parents=True)
    (feature / "spec.md").write_text("# Spec\n", encoding="utf-8")
    (feature / "tasks.md").write_text("# Tasks\n", encoding="utf-8")

    created = module.ensure_memory(root)
    text = (root / ".specify" / "memory" / "repository-governance.md").read_text(encoding="utf-8")

    assert created is True
    assert "- Feature specs: `specs/001-demo (spec.md:present, plan.md:missing, tasks.md:present)`" in text


def test_ensure_memory_initializes_from_repository_evidence(tmp_path):
    module = load_refresh_module()
    root = tmp_path
    (root / ".specify" / "extensions" / "repository-governance" / "templates").mkdir(parents=True)
    (root / ".specify" / "extensions" / "repository-governance" / "templates" / "repository-governance-template.md").write_text(
        TEMPLATE.read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    (root / ".specify" / "integration.json").write_text('{"default_integration": "codex"}', encoding="utf-8")
    (root / "README.md").write_text("# Evidence App\n\nA sample Spec Kit app.\n", encoding="utf-8")
    (root / "package.json").write_text(
        '{"scripts": {"test": "vitest run", "lint": "eslint ."}}',
        encoding="utf-8",
    )
    (root / "src").mkdir()
    (root / "tests").mkdir()
    (root / "AGENTS.md").write_text("# Agent Notes\n\nExisting user-authored context.\n", encoding="utf-8")

    created = module.ensure_memory(root)
    text = (root / ".specify" / "memory" / "repository-governance.md").read_text(encoding="utf-8")

    assert created is True
    assert "## Repository Evidence" in text
    assert_vertical_ssot_evidence(text)
    assert "- README: `README.md`" in text
    assert "- Package manifest: `package.json`" in text
    assert "- Test paths: `tests/`" in text
    assert "- Existing agent context files: `AGENTS.md`" in text
    assert "`npm test` -> `vitest run`" in text
    assert "`npm run lint` -> `eslint .`" in text
    assert "TODO(" not in text
