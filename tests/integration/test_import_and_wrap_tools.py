import asyncio
from collections.abc import Sequence
from typing import Any

import pytest
from agents.tool import Tool as OpenaiClass
from google.adk.tools import FunctionTool as GoogleClass
from langchain.tools import BaseTool as LangchainClass
from llama_index.core.tools import FunctionTool as LlamaindexClass
from smolagents.tools import Tool as SmolagentsClass

from any_agent import AgentFramework
from any_agent.config import Tool
from any_agent.tools import visit_webpage
from any_agent.tools.wrappers import import_and_wrap_tools


def import_and_wrap_sync(
    tools: Sequence[Tool],
    framework: AgentFramework,
) -> list[Tool]:
    wrapped_tools, _ = asyncio.get_event_loop().run_until_complete(
        import_and_wrap_tools(tools, framework),
    )
    return wrapped_tools


@pytest.mark.parametrize(
    "framework,expected_class",
    [
        ("google", GoogleClass),
        ("langchain", LangchainClass),
        ("llama_index", LlamaindexClass),
        ("openai", OpenaiClass),
        ("smolagents", SmolagentsClass),
    ],
)
def test_import_and_wrap_tools(framework: str, expected_class: Any) -> None:
    wrapped_tools = import_and_wrap_sync(
        ["any_agent.tools.search_web", visit_webpage],
        AgentFramework(framework),
    )
    assert all(isinstance(tool, expected_class) for tool in wrapped_tools)
