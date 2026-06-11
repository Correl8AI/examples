from __future__ import annotations

import os

from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStreamableHTTP

from app.env import correl8_api_key, mcp_url, openai_api_key
from app.prompts import SYSTEM_PROMPT

LLM_MODEL = "openai:gpt-4o-mini"


def build_agent() -> Agent[None, str]:
    os.environ["OPENAI_API_KEY"] = openai_api_key()

    mcp_server = MCPServerStreamableHTTP(
        mcp_url(),
        headers={"Authorization": f"ApiKey {correl8_api_key()}"},
        timeout=30,
        read_timeout=120,
    )
    return Agent(
        LLM_MODEL,
        system_prompt=SYSTEM_PROMPT,
        toolsets=[mcp_server],
    )
