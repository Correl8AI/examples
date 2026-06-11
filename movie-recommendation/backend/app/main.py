from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from . import agent as agent_module
from .schemas import ChatMessage, ChatRequest, ChatResponse

logger = logging.getLogger(__name__)

CORS_ORIGINS = ["http://localhost:5173"]

_agent: agent_module.Agent[agent_module.ChatDeps, str] | None = None


@asynccontextmanager
async def lifespan(_app: FastAPI):
    global _agent
    _agent = agent_module.build_agent()
    yield


app = FastAPI(title="Movie recommendations", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health() -> dict[str, bool]:
    return {"ok": True}


@app.post("/api/chat", response_model=ChatResponse)
async def chat(body: ChatRequest) -> ChatResponse:
    if _agent is None:
        raise HTTPException(status_code=503, detail="Agent not ready")

    try:
        content = await agent_module.run_chat(
            _agent,
            messages=body.messages,
            user_id=body.user_id,
            interaction_id=body.interaction_id,
        )
    except Exception as exc:
        logger.exception("chat failed")
        raise HTTPException(status_code=502, detail=_format_error(exc)) from exc

    return ChatResponse(message=ChatMessage(role="assistant", content=content))


def _format_error(exc: BaseException) -> str:
    if isinstance(exc, BaseExceptionGroup):
        return "; ".join(_format_error(e) for e in exc.exceptions)
    if exc.__cause__:
        return f"{exc}: {exc.__cause__}"
    return str(exc)
