"""Tools for managing MCP (Model Context Protocol) connections and resources."""

import os

from any_agent.config import MCPTool

from .mcp_server_base import MCPServerBase


class GoogleMCPServerStdio(MCPServerBase):
    """Implementation of MCP tools manager for Google agents."""

    def __init__(self, mcp_tool: MCPTool):
        super().__init__(mcp_tool)
        self.server = None

    async def setup_tools(self):
        """Set up the Google MCP server with the provided configuration."""
        from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset as GoogleMCPToolset
        from google.adk.tools.mcp_tool.mcp_toolset import (
            StdioServerParameters as GoogleStdioServerParameters,
        )

        params = GoogleStdioServerParameters(
            command=self.mcp_tool.command,
            args=self.mcp_tool.args,
            env={**os.environ},
        )

        toolset = GoogleMCPToolset(connection_params=params)
        await toolset.__aenter__()
        tools = await toolset.load_tools()
        self.tools = tools
        self.server = toolset
