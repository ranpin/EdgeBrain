"""
Test script for EdgeBrain MCP Client.
This script verifies the connection and tool discovery capabilities.
"""

import asyncio
import sys
import os

# Add src to path for local testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from edgebrain.core.mcp_client import MCPClient
from loguru import logger


async def main():
    # Example: Connect to a simple echo server or filesystem server
    # For this test, we'll assume a hypothetical 'mcp-server-echo' command exists
    # In a real scenario, you might point to a local Python script acting as an MCP server
    
    logger.info("Starting MCP Client Test...")
    
    # Note: This is a placeholder configuration. 
    # In a real environment, replace with an actual MCP server command.
    client = MCPClient(
        command="python", 
        args=["-m", "mcp_server_example"] # Placeholder for a real server module
    )

    try:
        await client.connect()
        
        # 1. List Tools
        tools = await client.list_tools()
        logger.info(f"Available Tools: {tools}")
        
        # 2. Call a Tool (if any exist)
        if tools:
            first_tool_name = tools[0]['name']
            logger.info(f"Attempting to call tool: {first_tool_name}")
            # result = await client.call_tool(first_tool_name, {"query": "hello"})
            # logger.info(f"Tool Result: {result}")
            
    except Exception as e:
        logger.error(f"Test failed: {e}")
    finally:
        await client.disconnect()
        logger.info("Test finished.")


if __name__ == "__main__":
    asyncio.run(main())
