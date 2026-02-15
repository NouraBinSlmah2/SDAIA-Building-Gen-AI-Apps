"""
Lab 4: MCP Server — Expose Tools via Model Context Protocol
=============================================================
Wrap the ToolRegistry in a FastMCP server so any MCP-compliant
client can discover and use your tools.

Prerequisites: Copy your Lab 3 files (or solutions) into this directory:
  base.py, calculator_tool.py, registry.py, manager.py, security.py, filesystem.py

Steps:
  1. Initialize the registry with tools
  2. Create a FastMCP server
  3. Add @mcp.tool() decorators that delegate to the registry
  4. Add a @mcp.resource() for system logs
  5. Run the server
"""

from mcp.server.fastmcp import FastMCP

# Import from Lab 3 (copy these files into this directory)
from base import BaseTool
from calculator_tool import CalculatorTool
from filesystem import ListFilesTool
from registry import ToolRegistry

# =============================================================================
# Step 1: Initialize the Registry
# =============================================================================
registry = ToolRegistry()
registry.register(CalculatorTool())
registry.register(ListFilesTool())

# =============================================================================
# Step 2: Create the MCP Server
# =============================================================================
mcp = FastMCP("Research Assistant Tools")

# =============================================================================
# Step 3: Expose Tools via MCP
# =============================================================================

# TODO: Create a @mcp.tool() function for calculate
# It should accept operation (str), operand_a (float), operand_b (float)
# and delegate to registry.execute("execute_calculation", {...})
#
# @mcp.tool()
# def calculate(operation: str, operand_a: float, operand_b: float) -> dict:
#     """Executes a calculation using the internal ToolRegistry."""
#     return registry.execute("execute_calculation", {
#         "operation": operation,
#         "operand_a": operand_a,
#         "operand_b": operand_b
#     })

# TODO: Create a @mcp.tool() function for list_files
# It should accept path (str) and delegate to registry.execute("list_files", {...})

# =============================================================================
# Step 4: Add a Resource
# =============================================================================

# TODO: Create a @mcp.resource() for "system://logs/recent"
# It should read the last 10 lines of "app.log" (or return "No logs available.")
#
# @mcp.resource("system://logs/recent")
# def get_recent_logs() -> str:
#     """Reads the last 10 lines of the application log."""
#     try:
#         with open("app.log", "r") as f:
#             lines = f.readlines()
#             return "".join(lines[-10:])
#     except FileNotFoundError:
#         return "No logs available."

# =============================================================================
# Step 5: Run the Server
# =============================================================================
if __name__ == "__main__":
    mcp.run()
