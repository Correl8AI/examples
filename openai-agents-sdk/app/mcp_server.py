from __future__ import annotations

from agents.mcp import MCPServerStreamableHttp

from app.env import correl8_api_key, mcp_url


def build_mcp_server() -> MCPServerStreamableHttp:
    return MCPServerStreamableHttp(
        params={
            "url": mcp_url(),
            "headers": {"Authorization": f"ApiKey {correl8_api_key()}"},
        },
        name="correl8",
    )
