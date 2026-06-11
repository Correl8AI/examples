# Correl8 examples

Correl8 helps teams building user-facing AI agents turn conversations into product observations.

These examples show how to give an agent a simple capability: when it notices friction, confusion, bugs, feature requests, or delight, it can post a structured observation to Correl8.

## Prerequisites

1. A [Correl8](https://app.correl8.ai) workspace and project (free plan is enough)
2. A project API key — open your project → **Settings** → create/copy a key → `CORREL8_API_KEY`
3. `CORREL8_PROJECT_ID` from your project URL: `/project/{project_id}/...`
4. An `OPENAI_API_KEY`

Each example includes its own `.env.example` (or `local/.env.example` for movie-recommendation). Copy it to `.env` before running.

CLI quick starts send the same scripted user message — see each example README for the exact text.

The same values work across examples — you can reuse one filled `.env` if you copy it into other example folders.

## Verify

After running an example, check Observations in Correl8:

```text
https://app.correl8.ai/project/{CORREL8_PROJECT_ID}/observations
```

## Quick starts (CLI)

| Example | Integration | Start here |
| ------- | ----------- | ---------- |
| [basic-agent](./basic-agent/) | REST custom tool | **Yes** |
| [langchain-agent-observations](./langchain-agent-observations/) | LangChain + MCP | |
| [openai-agents-sdk](./openai-agents-sdk/) | OpenAI Agents SDK + MCP | |
| [pydantic-ai-agent](./pydantic-ai-agent/) | Pydantic AI + MCP | |

## Full demo app

| Example | Description |
| ------- | ----------- |
| [movie-recommendation](./movie-recommendation/) | Browser chat app → agent → `post_observation` → Correl8 |

## License

MIT — see [LICENSE](./LICENSE).
