from __future__ import annotations

import asyncio

from pydantic_ai.messages import ToolCallPart

from app.agent import build_agent
from app.env import USER_MESSAGE, verify_url


async def run_demo() -> None:
    agent = build_agent()
    print(f"User: {USER_MESSAGE}")

    async with agent.run_mcp_servers():
        result = await agent.run(USER_MESSAGE)

    for message in result.all_messages():
        for part in message.parts:
            if isinstance(part, ToolCallPart) and part.tool_name == "post_observation":
                args = part.args if isinstance(part.args, dict) else {}
                print("Tool call: post_observation")
                print(f"  title: {args.get('title')}")
                print(f"  user_sentiment: {args.get('user_sentiment')}")

    if result.output:
        print(f"Agent: {result.output}")

    print(f"Done. Check Observations in Correl8: {verify_url()}")


def main() -> None:
    asyncio.run(run_demo())


if __name__ == "__main__":
    main()
