"""Shared fixtures.

Default posture: replay mode, observability off. Tests must be free,
deterministic and runnable on every commit (PROJECT_PLAN.md section 19.5).

Tests that genuinely need the live API must be marked `@pytest.mark.live`,
which is excluded by default via addopts in pyproject.toml.

Status: SKELETON - real fixtures land with T-009.
"""

from __future__ import annotations

import os

import pytest


@pytest.fixture(autouse=True, scope="session")
def _test_env() -> None:
    """Force a safe, offline-by-default configuration for the whole session."""
    os.environ.setdefault("APP_ENV", "test")
    os.environ.setdefault("LLM_CACHE_MODE", "read")
    os.environ.setdefault("OBSERVABILITY_ENABLED", "false")
    os.environ.setdefault("OPENAI_API_KEY", "sk-dummy-for-tests")


# TODO(T-009): fixtures for
#   - settings override
#   - in-memory FAISS index seeded with a tiny fixture corpus
#   - fake LLM client backed by the replay cache
#   - mcp_tools client pointed at fixture mock data
#   - case loader for data/evaluation/test_cases.json
