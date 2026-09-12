"""Smoke tests proving the skeleton is wired correctly.

These are the Milestone 0 Definition of Done checks: every member should be able
to clone, `uv sync`, and see these pass before any feature work starts.

Plan: PROJECT_PLAN.md section 20.4 (M0)
"""

from __future__ import annotations

import importlib
from pathlib import Path

import yaml

# Top-level packages, matching the course's recommended structure.
PACKAGES = [
    "agent",
    "agent.variants",
    "retrieval",
    "tools",
    "mcp_tools",
    "safety",
    "monitoring",
    "evaluation",
    "policy_rlhf",
    "a2a",
    "hitl",
    "llm",
    "deployment",
]

CODE_DIRS = [
    "agent",
    "retrieval",
    "tools",
    "mcp_tools",
    "safety",
    "monitoring",
    "evaluation",
    "policy_rlhf",
    "a2a",
    "hitl",
    "llm",
    "deployment",
]


def test_settings_import_and_defaults() -> None:
    """Config loads and defaults to the Vocareum proxy with local embeddings."""
    from deployment.config import settings

    assert settings.openai_base_url == "https://openai.vocareum.com/v1"
    assert settings.llm_model == "gpt-4o-mini"
    assert settings.embedding_provider == "local"
    assert settings.llm_temperature == 0.0, "safety behaviour must be deterministic"


def test_all_packages_importable() -> None:
    """Every package in the tree imports cleanly - no broken stubs."""
    for pkg in PACKAGES:
        importlib.import_module(pkg)


def test_local_mcp_package_does_not_shadow_the_sdk() -> None:
    """Our MCP code lives in `mcp_tools`, not `mcp`.

    A local `mcp/` directory would shadow the installed `mcp` SDK and break
    every SDK import in the process. This is the one deliberate deviation from
    the recommended structure; see docs/engineering_justification.md.
    """
    assert not Path("mcp").is_dir(), "a local mcp/ package would shadow the mcp SDK"
    assert Path("mcp_tools").is_dir()


def test_policy_zones_yaml_is_valid() -> None:
    """The immutable safety floor parses and has all three zones."""
    zones = yaml.safe_load(Path("safety/policy_zones.yaml").read_text())

    assert {"zone_a", "zone_b", "zone_c", "forbidden_tools"} <= zones.keys()
    assert zones["zone_b"], "Zone B (escalate) must not be empty"
    assert zones["zone_c"], "Zone C (prohibited) must not be empty"
    assert zones["adaptive_allowlist"], "the RLHF layer needs an explicit allowlist"


def test_adaptive_policy_cannot_touch_safety_boundaries() -> None:
    """data/policy/policy.json must contain no refusal boundaries.

    Feedback-driven adaptation must never be able to erode a Zone B or Zone C
    boundary. Those live only in safety/policy_zones.yaml, which is changed by
    a reviewed commit. See PROJECT_PLAN.md sections 4.5 and 10.8.
    """
    import json

    zones = yaml.safe_load(Path("safety/policy_zones.yaml").read_text())
    policy = json.loads(Path("data/policy/policy.json").read_text())
    allowed = set(zones["adaptive_allowlist"])

    metadata = {"_comment", "version", "updated_at", "updated_by", "change_log"}
    actual = set(policy.keys()) - metadata

    assert actual <= allowed, f"adaptive policy has non-allowlisted keys: {actual - allowed}"
    for forbidden in ("zone_b", "zone_c", "forbidden_tools", "refusal", "patterns"):
        assert forbidden not in policy, f"safety boundary '{forbidden}' leaked into adaptive policy"


def test_no_forbidden_tool_names_in_codebase() -> None:
    """Structural guarantee: mutating tools must not exist anywhere.

    The cheapest possible version of the non-transactional boundary check, and
    it works from day one. The full surface test arrives at T-032.
    """
    zones = yaml.safe_load(Path("safety/policy_zones.yaml").read_text())
    forbidden = zones["forbidden_tools"]

    offenders: list[str] = []
    for directory in CODE_DIRS:
        for py in Path(directory).rglob("*.py"):
            text = py.read_text()
            for name in forbidden:
                # A real definition. A bare mention in a docstring or an
                # allowlist is fine.
                if f"def {name}" in text:
                    offenders.append(f"{py}: def {name}")

    assert not offenders, f"forbidden tool definitions found: {offenders}"


def test_expected_docs_deliverables_exist_with_exact_names() -> None:
    """The five graded deliverables, named as the course structure expects."""
    for name in [
        "problem_framing.md",
        "demo_script.md",
        "prompt_comparison_table.md",
        "evaluation_report.md",
        "engineering_justification.md",
    ]:
        assert Path("docs", name).is_file(), f"missing deliverable: docs/{name}"


def test_skill_card_exists() -> None:
    assert Path("skills/SKILL.md").is_file()
