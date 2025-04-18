"""Tools for managing MCP (Model Context Protocol) connections and resources."""

from abc import ABC, abstractmethod
from contextlib import suppress
from typing import TYPE_CHECKING

from any_agent.config import MCPParams, MCPSseParams, MCPStdioParams, Tool

if TYPE_CHECKING:
    from collections.abc import Sequence


mcp_available = False
with suppress(ImportError):

    mcp_available = True


class MCPServerBase(ABC):
    """Base class for MCP tools managers across different frameworks."""

    def __init__(self, mcp_tool: MCPParams):
        if not mcp_available:
            msg = "You need to `pip install 'any-agent[mcp]'` to use MCP tools."
            raise ImportError(msg)

        # Store the original tool configuration
        self.mcp_tool = mcp_tool

        # Initialize tools list (to be populated by subclasses)
        self.tools: Sequence[Tool] = []

    @abstractmethod
    async def setup_tools(self) -> None:
        """Set up tools. To be implemented by subclasses."""
        match self.mcp_tool:
            case MCPStdioParams():
                await self.setup_stdio_tools()
            case MCPSseParams():
                await self.setup_sse_tools()

    @abstractmethod
    async def setup_sse_tools(self) -> None:
        """Set up tools. To be implemented by subclasses."""

    @abstractmethod
    async def setup_stdio_tools(self) -> None:
        """Set up tools. To be implemented by subclasses."""
