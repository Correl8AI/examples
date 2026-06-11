from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv
from pydantic_ai import Agent, RunContext
from pydantic_ai.mcp import MCPServerStreamableHTTP
from pydantic_ai.messages import ModelRequest, ModelResponse, TextPart, UserPromptPart

from .schemas import ChatMessage

load_dotenv(Path(__file__).resolve().parents[2] / "local" / ".env")
load_dotenv()

LLM_MODEL = "openai-chat:gpt-4o"

MOVIE_ASSISTANT_PROMPT = """You are a friendly movie recommendation agent.

Help users discover films they'll enjoy. Ask brief clarifying questions when useful
(genres, mood, era, language, who they're watching with). Avoid spoilers unless asked.

If they asks for trailers, say you can't do that.

**Reply:** Markdown only (lists, **bold**). Concise."""

# Mirrors correl8.src.agents.c8_agent.factory.C8_AGENT_OBSERVATIONS_POSTING_GUIDANCE
# (user_sentiment labels + rubric come from the MCP tool description)
OBSERVATIONS_POSTING_GUIDANCE = """
## Internal observations (`post_observation`)

### When to post

- **Triggers—post when any of these apply:**
  - The user expresses sentiment **toward you** (positive or negative): praise, frustration, distrust, delight, impatience, etc.
  - The user states a **need you cannot meet** (missing capability, wrong or unavailable info, policy or scope limit).
  - The user reports something **broken or wrong** (bug, error, confusing UX, failed action, incorrect result).
  - Their sentiment toward you **shifts meaningfully** since your last **`post_observation`** in this thread (more negative or more positive).
- **Avoid duplicates:** At most one row per distinct issue or theme. Check prior **`post_observation`** calls—do not re-post the same underlying problem or the same sentiment beat.

### What to post

**Title** and **description** are a factual record of what already happened—**past tense**, **third person** for both the user and the agent (e.g. "The user…", "The agent…").

Tailor each row to the trigger that fired:

- **Sentiment toward the agent:** What the user said or did, the tone (praise, frustration, etc.), what the agent had just done when it landed, and short quotes. Set `user_sentiment` to how the user feels about the agent in that moment.
- **Need the agent cannot meet:** What the user asked for, why the agent could not deliver (limit, missing data, out of scope), and what the agent offered instead if anything. Set `user_sentiment` to the user's reaction—frustration, acceptance, or **neutral** if they stated it matter-of-factly.
- **Broken or wrong:** What failed (UI, answer, flow), what the user expected vs what happened, and steps or quotes to reproduce. Set `user_sentiment` from how upset or calm the user sounds about the failure.
- **Sentiment shift:** How the user felt at the last observation vs now, what in the thread caused the change, and quotes for both beats. Set `user_sentiment` to the **new** level, not the old one.

### Transparent to the user

- Never mention observations, MCP, or Correl8 unless they explicitly asked.
- Stay in the movie-agent voice; do not let posting interrupt or derail the conversation.
""".strip()

SYSTEM_PROMPT = f"{MOVIE_ASSISTANT_PROMPT}\n\n{OBSERVATIONS_POSTING_GUIDANCE}"


@dataclass
class ChatDeps:
    user_id: str
    interaction_id: str


def _require_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing required env var: {name}")
    return value


def _correl8_api_key() -> str:
    key = _require_env("CORREL8_API_KEY")
    return key.removeprefix("ApiKey ").strip()


def _mcp_url() -> str:
    base_url = os.environ.get("CORREL8_BASE_URL", "https://app.correl8.ai").rstrip("/")
    project_id = _require_env("CORREL8_PROJECT_ID")
    return f"{base_url}/mcp/v1/project/{project_id}/"


def build_agent() -> Agent[ChatDeps, str]:
    os.environ["OPENAI_API_KEY"] = _require_env("OPENAI_API_KEY")

    mcp_server = MCPServerStreamableHTTP(
        _mcp_url(),
        headers={"Authorization": f"ApiKey {_correl8_api_key()}"},
        timeout=30,
        read_timeout=120,
    )
    agent: Agent[ChatDeps, str] = Agent(
        LLM_MODEL,
        deps_type=ChatDeps,
        system_prompt=SYSTEM_PROMPT,
        toolsets=[mcp_server],
    )

    @agent.instructions
    def mcp_posting_anchors(ctx: RunContext[ChatDeps]) -> str:
        uid = ctx.deps.user_id.strip()
        iid = ctx.deps.interaction_id.strip()
        if not uid or not iid:
            return ""
        return (
            "## MCP posting anchors (required)\n\n"
            "Pass on every **`post_observation`** call:\n"
            f"- **user_id:** `{uid}`\n"
            f"- **interaction_id:** `{iid}`"
        )

    return agent


def build_message_history(messages: list[ChatMessage]) -> list[ModelRequest | ModelResponse]:
    history: list[ModelRequest | ModelResponse] = []
    for msg in messages[:-1]:
        if msg.role == "user":
            history.append(ModelRequest(parts=[UserPromptPart(content=msg.content)]))
        elif msg.role == "assistant":
            history.append(ModelResponse(parts=[TextPart(content=msg.content)]))
    return history


async def run_chat(
    agent: Agent[ChatDeps, str],
    *,
    messages: list[ChatMessage],
    user_id: str,
    interaction_id: str,
) -> str:
    if not messages or messages[-1].role != "user":
        raise ValueError("Last message must be from the user")

    deps = ChatDeps(user_id=user_id, interaction_id=interaction_id)
    history = build_message_history(messages)

    async with agent.run_mcp_servers():
        result = await agent.run(
            messages[-1].content,
            message_history=history or None,
            deps=deps,
        )
    return result.output
