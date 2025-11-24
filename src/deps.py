from functools import cache
from typing import Annotated, Any

from agno.agent import Agent
from agno.models.litellm.litellm_openai import LiteLLMOpenAI
from agno.tools.hackernews import HackerNewsTools
from fastapi import Depends

from src.settings import Settings
from src.tools import get_latest_payment_status


@cache
def get_settings() -> Settings:
    return Settings()


@cache
def get_tools():
    return [get_latest_payment_status, HackerNewsTools()]


@cache
def get_litellm(
    settings: Annotated[Settings, Depends(get_settings)],
    llm_model: None | str = None,
):
    llm_model = llm_model if llm_model is not None else settings.llm_model
    return LiteLLMOpenAI(
        id=llm_model,
        base_url=settings.litellm_base_url,
        api_key=settings.litellm_key,
    )


def get_agent(
    settings: Annotated[Settings, Depends(get_settings)],
    litellm: Annotated[LiteLLMOpenAI, Depends(get_litellm)],
    tools: Annotated[list[Any], Depends(get_tools)],
):
    return Agent(
        id=settings.agent_id,
        name=settings.agent_name,
        model=litellm,
        tools=tools,
        markdown=True,
        debug_level=settings.debug_level,
    )
