# langchain-agent-observations

LangChain agent that calls Correl8 MCP `post_observation` during a scripted conversation.

## Run

```bash
cd langchain-agent-observations
uv sync
cp .env.example .env
# set CORREL8_MCP_URL, CORREL8_API_KEY, OPENAI_API_KEY
uv run python -m app.demo
```

## Scripted message

The demo sends this user message to a SaaS onboarding assistant:

> I tried inviting my teammate but could not find the button anywhere.

The agent should call `post_observation` with negative sentiment about the missing invite flow.

## What it does

1. Loads `post_observation` from Correl8 MCP via LangChain
2. Runs one scripted turn with a LangGraph ReAct agent
3. Prints any `post_observation` tool call

## Verify

```text
https://app.correl8.ai/project/{project_id}/observations
```

Look for an observation about the teammate invite flow.

## Note

For the simplest integration path (REST custom tool, no MCP client), see [basic-agent](../basic-agent/).
