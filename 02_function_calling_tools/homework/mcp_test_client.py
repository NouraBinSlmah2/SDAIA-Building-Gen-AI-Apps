"""
Homework: MCP Test Client
===========================
Connect to the converter MCP server and test the convert_currency tool.

Usage:
  1. In one terminal: python converter_template.py
  2. In another terminal: python mcp_test_client.py

Or just run this script — it will spawn the server automatically.
"""

import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def test_converter():
    """Connect to the converter server and test currency conversion."""

    server_params = StdioServerParameters(
        command="python",
        args=["converter_template.py"],
        env=None
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:

            # TODO: Initialize the session
            # await session.initialize()

            # TODO: List available tools and print them
            # tools = await session.list_tools()
            # print(f"Available tools: {[t.name for t in tools.tools]}")

            # TODO: Call convert_currency with:
            #   amount=100, from_currency="USD", to_currency="EUR"
            # result = await session.call_tool(
            #     "convert_currency",
            #     arguments={
            #         "amount": 100,
            #         "from_currency": "USD",
            #         "to_currency": "EUR"
            #     }
            # )
            # print(f"100 USD → EUR: {result.content[0].text}")

            # TODO: Try another conversion:
            #   amount=1000, from_currency="SAR", to_currency="GBP"

            print("MCP test client not yet implemented.")  # Remove this line


if __name__ == "__main__":
    asyncio.run(test_converter())
