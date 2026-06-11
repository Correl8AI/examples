# openai-agents-sdk

OpenAI Agents SDK agent with Correl8 MCP `post_observation`.

## Run

```bash
cd openai-agents-sdk
uv sync
cp .env.example .env
# set CORREL8_PROJECT_ID, CORREL8_API_KEY, OPENAI_API_KEY
uv run python -m app.demo
```

## Scripted message

The demo sends this user message to a SaaS onboarding assistant:

> I tried inviting my teammate but could not find the button anywhere.

The agent should call `post_observation` with negative sentiment about the missing invite flow.

## What it does

1. Connects to Correl8 MCP with the OpenAI Agents SDK
2. Runs one scripted turn
3. Prints the agent reply

## Verify

```text
https://app.correl8.ai/project/{CORREL8_PROJECT_ID}/observations
```

Look for an observation about the teammate invite flow.

## Note

For the simplest integration path (REST custom tool), see [basic-agent](../basic-agent/).
