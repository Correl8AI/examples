from __future__ import annotations

import asyncio

from app.agent import build_agent
from app.env import USER_MESSAGE, verify_url


async def run_demo() -> None:
    agent = await build_agent()
    print(f"User: {USER_MESSAGE}")
    result = await agent.ainvoke({"messages": [("user", USER_MESSAGE)]})

    for message in result["messages"]:
        tool_calls = getattr(message, "tool_calls", None) or []
        for tool_call in tool_calls:
            if tool_call.get("name") == "post_observation":
                args = tool_call.get("args", {})
                print("Tool call: post_observation")
                print(f"  title: {args.get('title')}")
                print(f"  user_sentiment: {args.get('user_sentiment')}")

    print(f"Done. Check Observations in Correl8: {verify_url()}")


def main() -> None:
    asyncio.run(run_demo())


if __name__ == "__main__":
    main()
