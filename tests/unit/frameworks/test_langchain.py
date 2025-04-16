from unittest.mock import MagicMock, patch

import pytest

from any_agent import AgentConfig, AgentFramework, AnyAgent
from any_agent.tools import (
    search_web,
    visit_webpage,
)


def test_load_langchain_agent_default() -> None:
    model_mock = MagicMock()
    create_mock = MagicMock()
    agent_mock = MagicMock()
    create_mock.return_value = agent_mock
    tool_mock = MagicMock()

    with (
        patch("any_agent.frameworks.langchain.create_react_agent", create_mock),
        patch("langchain_litellm.ChatLiteLLM", model_mock),
        patch("langchain_core.tools.tool", tool_mock),
    ):
        AnyAgent.create(AgentFramework.LANGCHAIN, AgentConfig(model_id="gpt-4o"))

        model_mock.assert_called_once_with(model="gpt-4o")
        create_mock.assert_called_once_with(
            name="any_agent",
            model=model_mock.return_value,
            tools=[tool_mock(search_web), tool_mock(visit_webpage)],
            prompt=None,
        )


def test_load_langchain_agent_missing() -> None:
    with patch("any_agent.frameworks.langchain.langchain_available", False):
        with pytest.raises(ImportError):
            AnyAgent.create(AgentFramework.LANGCHAIN, AgentConfig(model_id="gpt-4o"))


def test_load_langchain_multiagent() -> None:
    model_mock = MagicMock()
    create_mock = MagicMock()
    handoff_mock = MagicMock()

    def _create_effect(**kwargs: str) -> MagicMock:
        agent_mock = MagicMock()
        agent_mock.name = kwargs["name"]
        return agent_mock

    create_mock.side_effect = _create_effect
    tool_mock = MagicMock()

    with (
        patch("any_agent.frameworks.langchain.create_react_agent", create_mock),
        patch("any_agent.frameworks.langchain.create_handoff_tool", handoff_mock),
        patch("langchain_litellm.ChatLiteLLM", model_mock),
        patch("langchain_core.tools.tool", tool_mock),
    ):
        main_agent = AgentConfig(
            model_id="o3-mini",
        )
        managed_agents = [
            AgentConfig(
                model_id="gpt-4o",
                tools=[
                    "any_agent.tools.search_web",
                    "any_agent.tools.visit_webpage",
                ],
            ),
        ]

        AnyAgent.create(
            AgentFramework.LANGCHAIN,
            main_agent,
            managed_agents=managed_agents,
        )

        create_mock.assert_any_call(
            name="managed_agent_0",
            model=model_mock.return_value,
            tools=[
                tool_mock(search_web),
                tool_mock(visit_webpage),
                handoff_mock.return_value,
            ],
            prompt=None,
        )

        create_mock.assert_any_call(
            name="any_agent",
            model=model_mock.return_value,
            tools=[handoff_mock.return_value],
            prompt=None,
        )
