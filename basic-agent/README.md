# basic-agent

Smallest Correl8 integration: one custom agent tool that calls the public REST API.

No MCP. No framework beyond OpenAI tool calling.

## Run

```bash
cd basic-agent
uv sync
cp .env.example .env
# set CORREL8_PROJECT_ID, CORREL8_API_KEY, OPENAI_API_KEY
uv run python demo.py
```

## Scripted message

The demo sends this user message to a SaaS onboarding assistant:

> I tried inviting my teammate but could not find the button anywhere.

The agent should call `post_observation` with negative sentiment about the missing invite flow.

## What it does

1. Runs one scripted turn with OpenAI tool calling
2. Calls `post_observation` via the Correl8 public REST API
3. Prints the tool call and observation id

## Verify

```text
https://app.correl8.ai/project/{CORREL8_PROJECT_ID}/observations
```

Look for an observation about the teammate invite flow.

## Note

Framework examples in this repo use MCP instead. This example uses REST on purpose — it is the simplest integration path.
