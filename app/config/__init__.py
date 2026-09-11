"""Typed configuration. Re-exports the singleton settings object.

Plan: PROJECT_PLAN.md section 15
"""

from app.config.settings import Settings, settings

__all__ = ["Settings", "settings"]
