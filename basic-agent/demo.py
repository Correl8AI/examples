"""Minimal Correl8 integration: OpenAI tool calling + REST post_observation."""

from __future__ import annotations

import json
import os
import sys

import httpx
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

USER_ID = "demo-user-001"
INTERACTION_ID = "demo-interaction-001"
USER_MESSAGE = "I tried inviting my teammate but could not find the button anywhere."

POST_OBSERVATION_TOOL = {
    "type": "function",
    "function": {
        "name": "post_observation",
        "description": (
            "Record one product observation in Correl8. "
            "Use when the user reports friction, confusion, bugs, or missing features."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {"type": "string", "description": "Stable user identifier"},
                "interaction_id": {"type": "string", "description": "Conversation/session id"},
                "title": {"type": "string", "description": "Short factual summary"},
                "description": {
                    "type": "string",
                    "description": "Plain prose: what happened, why it matters, how to reproduce",
                },
                "user_sentiment": {
                    "type": "string",
                    "enum": [
                        "very negative",
                        "negative",
                        "neutral",
                        "positive",
                        "very positive",
                    ],
                    "description": "How the user feels in this moment",
                },
            },
            "required": [
                "user_id",
                "interaction_id",
                "title",
                "description",
                "user_sentiment",
            ],
        },
    },
}


def _require_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing required env var: {name}")
    return value


def _settings() -> tuple[str, str, str, str]:
    base_url = os.environ.get("CORREL8_BASE_URL", "https://app.correl8.ai").rstrip("/")
    project_id = _require_env("CORREL8_PROJECT_ID")
    api_key = _require_env("CORREL8_API_KEY").removeprefix("ApiKey ").strip()
    openai_key = _require_env("OPENAI_API_KEY")
    return base_url, project_id, api_key, openai_key


def post_observation(
    base_url: str,
    project_id: str,
    api_key: str,
    *,
    user_id: str,
    interaction_id: str,
    title: str,
    description: str,
    user_sentiment: str,
) -> dict:
    url = f"{base_url}/v1/project/{project_id}/observations/"
    response = httpx.post(
        url,
        json={
            "user_id": user_id,
            "interaction_id": interaction_id,
            "title": title,
            "description": description,
            "user_sentiment": user_sentiment,
        },
        headers={"Authorization": f"ApiKey {api_key}"},
        timeout=30.0,
    )
    response.raise_for_status()
    return response.json()


def main() -> None:
    base_url, project_id, api_key, openai_key = _settings()
    client = OpenAI(api_key=openai_key)

    system_prompt = f"""You are a SaaS onboarding assistant. You help users set up their workspace and invite teammates.

When the user reports product friction, confusion, bugs, or missing features, call post_observation with a factual title and description in past tense.
Always pass user_id={USER_ID} and interaction_id={INTERACTION_ID}."""

    messages: list[dict] = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": USER_MESSAGE},
    ]

    print(f"User: {USER_MESSAGE}")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=[POST_OBSERVATION_TOOL],
    )
    assistant = response.choices[0].message

    if assistant.content:
        print(f"Agent: {assistant.content}")

    if not assistant.tool_calls:
        print("No post_observation call was made.")
        sys.exit(1)

    for tool_call in assistant.tool_calls:
        args = json.loads(tool_call.function.arguments)
        print("Tool call: post_observation")
        print(f"  title: {args.get('title')}")
        print(f"  user_sentiment: {args.get('user_sentiment')}")
        row = post_observation(base_url, project_id, api_key, **args)
        print(f"  observation_id: {row.get('id')}")

        messages.append(
            {
                "role": "assistant",
                "content": assistant.content,
                "tool_calls": [
                    {
                        "id": tool_call.id,
                        "type": "function",
                        "function": {
                            "name": tool_call.function.name,
                            "arguments": tool_call.function.arguments,
                        },
                    }
                ],
            }
        )
        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(row),
            }
        )

    verify_url = f"https://app.correl8.ai/project/{project_id}/observations"
    print(f"Done. Check Observations in Correl8: {verify_url}")


if __name__ == "__main__":
    main()
