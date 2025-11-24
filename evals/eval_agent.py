import os
import sys

from autoevals import Levenshtein
from braintrust import Eval, init_logger

sys.path.append(os.path.join(os.path.dirname(__file__), "../src"))

from deps import get_agent, get_litellm, get_settings, get_tools

init_logger(project="ai-agno-agent")


def create_test_agent():
    settings = get_settings()
    print("settings", settings)
    litellm = get_litellm(llm_model=None, settings=settings)
    tools = get_tools()

    return get_agent(settings=settings, litellm=litellm, tools=tools)


async def run_agent_task(input_data: str):
    agent = create_test_agent()
    response = await agent.arun(input_data)
    return response.content


def get_eval_data():
    return [
        {
            "input": "What is the payment status for client 123?",
            "expected": "The payment status for client 123 is CONFIRMED.",
        },
        {
            "input": "Hello, who are you?",
            "expected": "I am an AI agent.",
        },
    ]


Eval(
    "Agno Agent Evaluation",
    data=get_eval_data,
    task=run_agent_task,
    scores=[
        Levenshtein,
    ],
)
