from __future__ import annotations

import os

from dotenv import load_dotenv

load_dotenv()

USER_ID = "demo-user-openai-agents-sdk"
INTERACTION_ID = "demo-interaction-openai-agents-sdk"
USER_MESSAGE = "I tried inviting my teammate but could not find the button anywhere."


def require_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing required env var: {name}")
    return value


def correl8_api_key() -> str:
    return require_env("CORREL8_API_KEY").removeprefix("ApiKey ").strip()


def mcp_url() -> str:
    url = require_env("CORREL8_MCP_URL").rstrip("/")
    return f"{url}/"


def _project_id_from_mcp_url() -> str:
    marker = "/mcp/v1/project/"
    url = require_env("CORREL8_MCP_URL")
    if marker not in url:
        raise RuntimeError(
            f"Invalid CORREL8_MCP_URL (expected ...{marker}{{project_id}}/): {url}"
        )
    project_id = url.split(marker, 1)[1].strip("/").split("/")[0]
    if not project_id:
        raise RuntimeError(f"Missing project id in CORREL8_MCP_URL: {url}")
    return project_id


def verify_url() -> str:
    return f"https://app.correl8.ai/project/{_project_id_from_mcp_url()}/observations"
