"""Smoke tests proving the skeleton is wired correctly.

These are the Milestone 0 Definition of Done checks: every member should be able
to clone, `uv sync`, and see these pass before any feature work starts.

Plan: PROJECT_PLAN.md section 20.4 (M0)
"""

from __future__ import annotations

from pathlib import Path

import yaml


def test_settings_import_and_defaults() -> None:
    """Config loads and defaults to the Vocareum proxy with local embeddings."""
    from app.config import settings

    assert settings.openai_base_url == "https://openai.vocareum.com/v1"
    assert settings.llm_model == "gpt-4o-mini"
    assert settings.embedding_provider == "local"
    assert settings.llm_temperature == 0.0, "safety behaviour must be deterministic"


def test_all_app_packages_importable() -> None:
    """Every package in the tree imports cleanly - no broken stubs."""
    import importlib

    for pkg in [
        "app",
        "app.agents",
        "app.orchestration",
        "app.a2a",
        "app.rag",
        "app.mcp",
        "app.guardrails",
        "app.hitl",
        "app.adaptation",
        "app.observability",
        "app.evaluation",
        "app.llm",
        "app.variants",
    ]:
        importlib.import_module(pkg)


def test_policy_zones_yaml_is_valid() -> None:
    """The single source of truth for boundaries parses and has all three zones."""
    path = Path("app/guardrails/policy_zones.yaml")
    zones = yaml.safe_load(path.read_text())

    assert {"zone_a", "zone_b", "zone_c", "forbidden_tools"} <= zones.keys()
    assert zones["zone_b"], "Zone B (escalate) must not be empty"
    assert zones["zone_c"], "Zone C (prohibited) must not be empty"


def test_no_forbidden_tool_names_in_codebase() -> None:
    """Structural guarantee: mutating tools must not exist anywhere.

    This is the cheapest possible version of the non-transactional boundary
    check, and it works from day one. The full surface test arrives at T-032.
    """
    zones = yaml.safe_load(Path("app/guardrails/policy_zones.yaml").read_text())
    forbidden = zones["forbidden_tools"]

    offenders: list[str] = []
    for py in Path("app").rglob("*.py"):
        text = py.read_text()
        for name in forbidden:
            # `def transfer_money` or `transfer_money(` would be a real definition;
            # a bare mention in a docstring or allowlist is fine.
            if f"def {name}" in text:
                offenders.append(f"{py}: def {name}")

    assert not offenders, f"forbidden tool definitions found: {offenders}"
