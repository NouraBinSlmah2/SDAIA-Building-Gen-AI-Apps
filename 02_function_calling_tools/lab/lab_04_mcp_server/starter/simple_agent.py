"""
Lab 4: MCP Client — Connect to the MCP Server
================================================
Build a simple MCP client that:
  1. Spawns the server as a subprocess
  2. Connects via stdio transport
  3. Lists available tools
  4. Calls the calculate tool
  5. Prints the result

Steps:
  1. Define StdioServerParameters to spawn server.py
  2. Connect with stdio_client and ClientSession
  3. Initialize the session
  4. List tools
  5. Call a tool and print the result
"""

import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def run_agent():
    """Connect to the MCP server and interact with tools."""

    # Step 1: Define how to start the server
    server_params = StdioServerParameters(
        command="python",
        args=["server.py"],  # Adjust path if needed
        env=None
    )

    # Step 2: Connect to the server via stdio
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:

            # TODO Step 3: Initialize the connection
            # await session.initialize()

            # TODO Step 4: List available tools
            # tools = await session.list_tools()
            # print(f"Connected! Server provides {len(tools.tools)} tools:")
            # for tool in tools.tools:
            #     print(f"  - {tool.name}: {tool.description}")

            # TODO Step 5: Call the calculate tool
            # result = await session.call_tool(
            #     "calculate",
            #     arguments={
            #         "operation": "add",
            #         "operand_a": 10,
            #         "operand_b": 5
            #     }
            # )
            # print(f"\nResult: {result.content[0].text}")

            print("MCP client not yet implemented.")  # Remove this line


if __name__ == "__main__":
    asyncio.run(run_agent())
