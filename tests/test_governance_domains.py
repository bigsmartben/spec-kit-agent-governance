import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "templates" / "agent-governance-template.md"
SCRIPT = ROOT / "scripts" / "refresh_agent_governance.py"


def load_refresh_module():
    spec = importlib.util.spec_from_file_location("refresh_agent_governance", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def assert_agent_governance_domain_only(text: str) -> None:
    assert "agent collaboration rules" in text
    assert "tool and MCP permissions" in text
    assert "write boundaries" in text
    assert "skill invocation contracts" in text

    assert ".specify/memory/constitution.md" not in text
    assert ".specify/memory/architecture.md" not in text
    assert ".specify/memory/uc.md" not in text
    assert "specs/<feature>" not in text
    assert "Feature Specs" not in text
    assert "required spec workflow" not in text
    assert "code-write gate" not in text


def test_template_defines_decoupled_agent_governance_ssot():
    text = TEMPLATE.read_text(encoding="utf-8")

    assert_agent_governance_domain_only(text)
    assert "Project Governance Domain" in text
    assert "independent" in text


def test_projection_defines_decoupled_agent_governance_ssot(tmp_path):
    module = load_refresh_module()
    root = tmp_path
    memory = root / ".specify" / "memory"
    memory.mkdir(parents=True)
    (memory / "agent-governance.md").write_text(TEMPLATE.read_text(encoding="utf-8"), encoding="utf-8")

    projection = module.render_projection(root, root / "AGENTS.md", {"default_integration": "codex"}, False)

    assert_agent_governance_domain_only(projection)
    assert "Project Governance Domain" in projection
    assert "Constitution" not in projection
