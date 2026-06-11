from __future__ import annotations

from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from app.env import openai_api_key
from app.mcp_tools import load_correl8_tools
from app.prompts import SYSTEM_PROMPT


async def build_agent():
    tools = await load_correl8_tools()
    llm = ChatOpenAI(model="gpt-4o-mini", api_key=openai_api_key())
    return create_react_agent(llm, tools, prompt=SYSTEM_PROMPT)
