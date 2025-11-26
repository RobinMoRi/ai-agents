import os
import sys

from autoevals import Levenshtein, Possible
from braintrust import Eval, init_logger, traced
from braintrust.wrappers.agno import setup_agno

sys.path.append(os.path.join(os.path.dirname(__file__), "../src"))

from deps import get_agent, get_litellm, get_settings, get_tools

settings = get_settings()
setup_agno(project_name="ai-agno-agent", api_key=settings.braintrust_api_key)
logger = init_logger(project="ai-agno-agent")


def create_test_agent():
    settings = get_settings()
    litellm = get_litellm(llm_model=None, settings=settings)
    tools = get_tools()

    return get_agent(settings=settings, litellm=litellm, tools=tools)


def check_tool_calls(output, expected):
    expected_tools = expected.get("tool_calls", [])
    actual_tools = output.get("tool_calls", [])
    return 1 if set(expected_tools) == set(actual_tools) else 0


def check_content(output, expected):
    return Levenshtein()(output["content"], expected["content"]).score


@traced
def check_possible(input, output, expected):
    settings = get_settings()
    return Possible(
        model="gpt-4o",
        api_key=settings.litellm_key,
        base_url=settings.litellm_base_url,
    )(output=output, input=input).score


async def run_agent_task(input_data: str, _):
    agent = create_test_agent()
    response = await agent.arun(input_data)

    tool_calls = [tool.tool_name for tool in response.tools] if response.tools else []

    return {
        "content": response.content,
        "tool_calls": tool_calls,
    }


def get_eval_data():
    return [
        {
            "input": "What is the payment status for client 123?",
            "expected": {
                "content": "The payment status for client 123 is CONFIRMED.",
                "tool_calls": ["LatestPaymentStatusTool"],
            },
        },
        {
            "input": "Hello, who are you?",
            "expected": {
                "content": "I am an AI agent.",
                "tool_calls": [],
            },
        },
    ]


Eval(
    "ai-agno-agent",
    data=get_eval_data,
    task=run_agent_task,
    scores=[
        check_content,
        check_tool_calls,
        # check_possible,
    ],
)
