from __future__ import annotations

from langchain_mcp_adapters.client import MultiServerMCPClient

from app.env import correl8_api_key, mcp_url


async def load_correl8_tools():
    client = MultiServerMCPClient(
        {
            "correl8": {
                "transport": "streamable_http",
                "url": mcp_url(),
                "headers": {"Authorization": f"ApiKey {correl8_api_key()}"},
            }
        }
    )
    return await client.get_tools()
