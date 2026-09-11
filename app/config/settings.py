"""Typed application configuration.

This module is the ONLY place in the codebase that reads environment variables.
Everything else does `from app.config import settings`.

Rationale: config drift is the classic source of "works on my machine". A lint
test in tests/unit asserts that `os.getenv` appears nowhere outside this package.

Plan: PROJECT_PLAN.md section 15
Tasks: T-002
"""

from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Validated at import time. Fails loudly at startup, not mid-demo."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # --- LLM: Vocareum proxy by default, personal key is a 2-line swap ---
    llm_provider: Literal["openai_compatible", "openai", "ollama"] = "openai_compatible"
    openai_base_url: str = "https://openai.vocareum.com/v1"
    openai_api_key: SecretStr = SecretStr("")
    llm_model: str = "gpt-4o-mini"
    llm_temperature: float = 0.0
    llm_max_tokens: int = 1200
    llm_timeout_s: int = 30

    # --- Embeddings: local by default (free, offline, no allowance burn) ---
    embedding_provider: Literal["local", "openai"] = "local"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"

    # --- Vector store ---
    vector_store: Literal["chroma", "qdrant"] = "chroma"
    vector_store_path: Path = Path("./data/vectorstore")
    collection_name: str = "novabank_policies"

    # --- Retrieval ---
    retrieval_k: int = 8
    retrieval_min_score: float = 0.35
    min_citations: int = 2
    max_subquestions: int = 3

    # --- Thresholds ---
    event_confidence_threshold: float = 0.70
    high_value_threshold_eur: int = 10_000

    # --- A2A / MCP ---
    a2a_transport: Literal["http", "inproc"] = "http"
    policy_agent_url: str = "http://localhost:8001"
    a2a_deadline_ms: int = 15_000
    mcp_server_command: str = "python -m app.mcp.server"

    # --- Observability (degrades to NullTracer when disabled) ---
    observability_enabled: bool = False
    langfuse_public_key: SecretStr | None = None
    langfuse_secret_key: SecretStr | None = None
    langfuse_host: str = "https://cloud.langfuse.com"

    # --- App ---
    app_env: Literal["local", "demo", "test"] = "local"
    log_level: str = "INFO"

    # --- Feature flags ---
    enable_reranking: bool = False
    enable_adaptation: bool = True
    enable_llm_risk_advisor: bool = True
    llm_cache_mode: Literal["off", "read", "write", "readwrite"] = "readwrite"

    # --- Paths (not env-driven; derived project layout) ---
    @property
    def policies_dir(self) -> Path:
        return Path("./data/policies")

    @property
    def cache_dir(self) -> Path:
        return Path("./data/cache")


settings = Settings()
