"""
EdgeBrain 3.0 Pro - MCP Client Module
Implements Model Context Protocol client for standardized tool interoperability.
"""

import asyncio
from typing import Any, Dict, List, Optional
from loguru import logger
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class MCPClient:
    """
    Manages connection to an MCP server and provides methods for tool discovery and execution.
    """

    def __init__(self, command: str, args: List[str], env: Optional[Dict[str, str]] = None):
        self.command = command
        self.args = args
        self.env = env or {}
        self.session: Optional[ClientSession] = None
        self._client_context = None

    async def connect(self):
        """Establishes a connection to the MCP server."""
        try:
            server_params = StdioServerParameters(
                command=self.command,
                args=self.args,
                env=self.env
            )
            self._client_context = stdio_client(server_params)
            read_stream, write_stream = await self._client_context.__aenter__()
            
            self.session = ClientSession(read_stream, write_stream)
            await self.session.__aenter__()
            
            # Initialize the session
            await self.session.initialize()
            logger.info(f"MCP Client connected to {self.command} successfully.")
        except Exception as e:
            logger.error(f"Failed to connect to MCP server: {e}")
            raise

    async def list_tools(self) -> List[Dict[str, Any]]:
        """Discovers available tools from the connected MCP server."""
        if not self.session:
            raise RuntimeError("MCP Client is not connected.")
        
        response = await self.session.list_tools()
        tools = []
        for tool in response.tools:
            tools.append({
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.inputSchema
            })
        logger.info(f"Discovered {len(tools)} tools from MCP server.")
        return tools

    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> Any:
        """Calls a specific tool on the MCP server."""
        if not self.session:
            raise RuntimeError("MCP Client is not connected.")
        
        try:
            result = await self.session.call_tool(name, arguments)
            return result.content
        except Exception as e:
            logger.error(f"Error calling tool '{name}': {e}")
            raise

    async def disconnect(self):
        """Closes the connection to the MCP server."""
        if self.session:
            await self.session.__aexit__(None, None, None)
            self.session = None
        if self._client_context:
            await self._client_context.__aexit__(None, None, None)
            self._client_context = None
        logger.info("MCP Client disconnected.")
