# Lab 3: The Plugin Framework

**Module 02 — Function Calling & Tool Systems | Session 2, Parts 2 & 3**

## Overview

Refactor from ad-hoc functions to a scalable plugin architecture. You'll build an Abstract Base Class, a Tool Registry, rate limiting, security controls, and a filesystem tool — all pure Python OOP.

## Prerequisites

- Python 3.10+
- **No API keys needed** — this lab is pure Python

## Steps

1. **`base.py`** — Read the `BaseTool` ABC (provided — understand the contract)
2. **`calculator_tool.py`** — Migrate the calculator to `CalculatorTool(BaseTool)`
3. **`registry.py`** — Build `ToolRegistry` with register, get_schemas, execute
4. **`manager.py`** — Implement `ToolRateLimiter` (token bucket)
5. **`security.py`** — Build `PathSanitizer` to block directory traversal
6. **`filesystem.py`** — Build `ListFilesTool` with permissions, test security

## File Structure

```
starter/              # Your workspace — has TODOs to complete
  base.py             # BaseTool ABC (complete — read and understand)
  calculator_tool.py  # CalculatorTool migration (TODOs)
  registry.py         # ToolRegistry (TODOs)
  manager.py          # ToolRateLimiter (TODOs)
  security.py         # PathSanitizer (TODOs)
  filesystem.py       # ListFilesTool (TODOs)

solutions/            # Reference implementation
  base.py
  calculator_tool.py
  registry.py
  manager.py
  security.py
  filesystem.py
```

## Running

```bash
# Test registry with all tools
python solutions/registry.py
```

## Success Criteria

- `CalculatorTool` conforms to `BaseTool` and produces correct schemas
- `ToolRegistry` dynamically discovers and executes tools
- Rate limiter blocks calls that exceed the per-minute threshold
- `PathSanitizer` prevents `../../` directory traversal attacks
- `ListFilesTool` requires `filesystem:read` permission
