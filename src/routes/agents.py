from typing import Annotated

from agno.agent import Agent
from fastapi import APIRouter, Depends, Query

from deps import get_agent

router = APIRouter(prefix="/agents", tags=["Agents"])


@router.get("")
async def create_agent_call(
    agent: Annotated[Agent, Depends(get_agent)],
    input: str = Query(default=...),
):
    return await agent.arun(input=input)
