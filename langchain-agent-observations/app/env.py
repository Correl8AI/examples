"""Shared env loading for LangChain example."""

from __future__ import annotations

import os

from dotenv import load_dotenv

load_dotenv()

USER_ID = "demo-user-001"
INTERACTION_ID = "demo-interaction-001"
USER_MESSAGE = "I tried inviting my teammate but could not find the button anywhere."


def require_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing required env var: {name}")
    return value


def correl8_base_url() -> str:
    return os.environ.get("CORREL8_BASE_URL", "https://app.correl8.ai").rstrip("/")


def correl8_project_id() -> str:
    return require_env("CORREL8_PROJECT_ID")


def correl8_api_key() -> str:
    return require_env("CORREL8_API_KEY").removeprefix("ApiKey ").strip()


def openai_api_key() -> str:
    return require_env("OPENAI_API_KEY")


def mcp_url() -> str:
    return f"{correl8_base_url()}/mcp/v1/project/{correl8_project_id()}/"


def verify_url() -> str:
    return f"https://app.correl8.ai/project/{correl8_project_id()}/observations"
