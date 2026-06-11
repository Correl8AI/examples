# Movie recommendation demo

Minimal chat app (React + FastAPI + Pydantic AI) that recommends movies and connects to Correl8 MCP (`post_observation`).

## Prerequisites

1. A [Correl8](https://app.correl8.ai) project
2. Project API key — **Settings** → create/copy key → `CORREL8_API_KEY`
3. `CORREL8_PROJECT_ID` from your project URL
4. `OPENAI_API_KEY`

Copy `local/.env.example` → `local/.env` and fill in the values above.

## Run with Docker

```bash
cd movie-recommendation/local
cp .env.example .env
./start.sh
```

Open http://localhost:5173

## Run natively

```bash
# Backend (reads movie-recommendation/local/.env)
cd movie-recommendation/backend
uv sync
uv run uvicorn app.main:app --reload --port 8001

# Frontend (another terminal)
cd movie-recommendation/frontend
npm install
npm run dev
```

Health checks:

```bash
curl http://localhost:8001/health
```

## Demo script

Example conversation:

1. *"Hey there, I'm hosting a movie night with friends. I'm looking for an underrated classic comedy, suggest one."*
2. *"I love it! Show me the trailer"*
3. *"Useless bot"* — the agent cannot show trailers; this may trigger `post_observation`

To test product feedback directly, try: *"The send button didn't work when I pressed Enter"*

## Verify

```text
https://app.correl8.ai/project/{CORREL8_PROJECT_ID}/observations
```

## Self-hosted Correl8

Set `CORREL8_BASE_URL=http://localhost:8000` in `local/.env` (native) or `http://host.docker.internal:8000` (Docker).
