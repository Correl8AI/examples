from __future__ import annotations

import asyncio

from agents import Agent, Runner

from app.env import USER_MESSAGE, verify_url
from app.mcp_server import build_mcp_server
from app.prompts import SYSTEM_PROMPT


async def run_demo() -> None:
    server = build_mcp_server()
    async with server:
        agent = Agent(
            name="Onboarding assistant",
            instructions=SYSTEM_PROMPT,
            mcp_servers=[server],
        )
        print(f"User: {USER_MESSAGE}")
        result = await Runner.run(agent, USER_MESSAGE)
        if result.final_output:
            print(f"Agent: {result.final_output}")
    print(f"Done. Check Observations in Correl8: {verify_url()}")


def main() -> None:
    asyncio.run(run_demo())


if __name__ == "__main__":
    main()
