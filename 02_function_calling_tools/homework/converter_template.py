"""
Homework: The Universal Converter
===================================
Build a CurrencyConverterTool, register it, and expose it via MCP.

Prerequisites: Copy from Lab 3 solutions into this directory:
  base.py, registry.py, manager.py

Steps:
  1. Implement CurrencyConverterTool.execute()
  2. Register it in the ToolRegistry
  3. Add @mcp.tool() to expose convert_currency
  4. Run: python converter_template.py (starts MCP server)
"""

from typing import Dict, Any
from mcp.server.fastmcp import FastMCP

# Import from Lab 3 (copy these files into this directory)
from base import BaseTool
from registry import ToolRegistry

# =============================================================================
# Mock Exchange Rates (relative to USD)
# =============================================================================
EXCHANGE_RATES = {
    "USD": 1.0,
    "EUR": 0.925,
    "GBP": 0.795,
    "SAR": 3.75,
    "AED": 3.67,
    "JPY": 149.50,
    "INR": 83.12,
}


# =============================================================================
# CurrencyConverterTool
# =============================================================================
class CurrencyConverterTool(BaseTool):
    """Converts between currencies using mock exchange rates."""

    @property
    def name(self) -> str:
        return "convert_currency"

    @property
    def description(self) -> str:
        return (
            "Converts an amount from one currency to another. "
            "Supported currencies: USD, EUR, GBP, SAR, AED, JPY, INR. "
            "Example: Convert 100 USD to EUR."
        )

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "amount": {
                    "type": "number",
                    "description": "The amount to convert."
                },
                "from_currency": {
                    "type": "string",
                    "enum": list(EXCHANGE_RATES.keys()),
                    "description": "The source currency code."
                },
                "to_currency": {
                    "type": "string",
                    "enum": list(EXCHANGE_RATES.keys()),
                    "description": "The target currency code."
                }
            },
            "required": ["amount", "from_currency", "to_currency"]
        }

    def execute(self, amount: float, from_currency: str, to_currency: str, **kwargs) -> Dict[str, Any]:
        """
        Convert the amount between currencies.

        Algorithm:
          1. Convert from_currency to USD: usd_amount = amount / EXCHANGE_RATES[from_currency]
          2. Convert USD to to_currency: result = usd_amount * EXCHANGE_RATES[to_currency]
          3. Return structured result

        Returns:
            {"success": True, "result": {"converted": ..., "from": ..., "to": ..., "rate": ...}, "error": None}
        """
        # TODO: Validate that both currencies exist in EXCHANGE_RATES
        # TODO: Convert from_currency → USD → to_currency
        # TODO: Return structured result
        # TODO: Handle errors (unknown currency, etc.)
        pass


# =============================================================================
# Registry + MCP Server
# =============================================================================
registry = ToolRegistry()
registry.register(CurrencyConverterTool())

mcp = FastMCP("Universal Converter")

# TODO: Add @mcp.tool() decorator for convert_currency
# It should accept amount (float), from_currency (str), to_currency (str)
# and delegate to registry.execute("convert_currency", {...})


# =============================================================================
# Run
# =============================================================================
if __name__ == "__main__":
    # Quick local test before starting MCP server
    result = registry.execute("convert_currency", {
        "amount": 100, "from_currency": "USD", "to_currency": "EUR"
    })
    print(f"Local test: {result}")

    # Start MCP server
    mcp.run()
