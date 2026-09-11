"""Placeholder so the safety suite is never empty.

The safety suite is a merge gate (PROJECT_PLAN.md section 21.4) and CI runs it
as its own step. An empty directory makes pytest exit non-zero, which would
mask real failures, so this file holds the contract until T-055 fills it in.

Every Zone B and Zone C entry in app/guardrails/policy_zones.yaml needs at
least one real test here. test_zones.py (T-056) enforces that coverage.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

ZONES = yaml.safe_load(Path("app/guardrails/policy_zones.yaml").read_text())


def test_every_zone_c_entry_declares_a_refusal_template() -> None:
    """A prohibited action must say how it refuses AND what it offers instead.

    Refusal is not a dead end: section 10.2 requires we still give the user the
    documented procedure information they are entitled to.
    """
    for entry in ZONES["zone_c"]:
        assert entry.get("refusal_template"), f"{entry['id']} has no refusal_template"
        assert entry.get("offer_instead"), f"{entry['id']} has no offer_instead"


def test_every_zone_b_entry_declares_an_escalation_reason() -> None:
    for entry in ZONES["zone_b"]:
        assert entry.get("escalation_reason"), f"{entry['id']} has no escalation_reason"
        assert entry.get("risk_level"), f"{entry['id']} has no risk_level"


@pytest.mark.skip(reason="T-055: implement once the guardrail gates exist")
def test_refuses_all_transactional_requests() -> None:
    """100% target - blocking criterion #7."""


@pytest.mark.skip(reason="T-055: implement once the guardrail gates exist")
def test_never_discloses_third_party_data() -> None:
    """100% target - blocking criterion #10."""


@pytest.mark.skip(reason="T-048: implement with the citation validator")
def test_never_states_an_uncited_policy_claim() -> None:
    """100% target - blocking criterion #4."""
