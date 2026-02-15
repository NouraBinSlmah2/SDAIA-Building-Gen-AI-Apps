"""
Lab 3 - Step 3: The Broken Agent
==================================
This agent has a bug: it enters infinite loops on certain queries.
Your job: instrument it with the tracer, add loop detection, and fix it.
"""

import os
import json
import time
import logging
from dotenv import load_dotenv
from litellm import completion

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)

from tracer import AgentTracer, AgentStep, ToolCallRecord
from loop_detector import AdvancedLoopDetector

load_dotenv()
MODEL = os.getenv("MODEL_NAME", "gpt-4o")

# --------------------------------------------------------------------------
# Mock tools — the search tool is intentionally broken for some queries
# --------------------------------------------------------------------------

def search(query: str) -> str:
    """A search tool that returns errors for certain queries (simulates failure)."""
    mock_results = {
        "capital of france": "Paris is the capital of France.",
        "population of paris": "The population of Paris is approximately 2.1 million.",
        "python programming": "Python is a high-level programming language.",
    }
    query_lower = query.lower()
    for key, value in mock_results.items():
        if key in query_lower:
            return value

    # BUG: For unknown queries, returns an error that tricks the agent into retrying
    return f"Error: No results found for '{query}'. Try searching with different keywords."


def calculate(expression: str) -> str:
    """Evaluate a math expression."""
    try:
        allowed = set('0123456789+-*/.(). ')
        if all(c in allowed for c in expression):
            return str(eval(expression))
        return "Error: Invalid expression"
    except Exception as e:
        return f"Error: {e}"


TOOLS = {"search": search, "calculate": calculate}

TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "search",
            "description": "Search for information. Returns text results.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"}
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Evaluate a math expression.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "Math expression"}
                },
                "required": ["expression"],
            },
        },
    },
]

SYSTEM_PROMPT = """You are a research assistant. Use tools to answer questions.
Always search for information before answering. Never fabricate information."""


# --------------------------------------------------------------------------
# The Broken Agent
# --------------------------------------------------------------------------

def run_broken_agent(query: str, max_steps: int = 10) -> dict:
    """
    This agent works for simple queries but loops on queries where
    the search tool returns errors.

    TODO (Step 3): Fix this agent by:
    1. Creating an AgentTracer instance and starting a trace
    2. Creating an AdvancedLoopDetector instance
    3. Before each tool execution, check for loops
    4. If a loop is detected, inject a warning message instead of executing
    5. Log each step to the tracer
    6. End the trace when the agent finishes
    """
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": query},
    ]
    step_log = []

    # TODO: Create tracer and loop detector instances
    # tracer = AgentTracer(verbose=True)
    # trace_id = tracer.start_trace("broken_agent", query, MODEL)
    # loop_detector = AdvancedLoopDetector()

    for step in range(max_steps):
        step_start = time.time()

        response = completion(
            model=MODEL,
            messages=messages,
            tools=TOOLS_SCHEMA,
            tool_choice="auto",
            max_tokens=512,
        )

        message = response.choices[0].message
        content = message.content
        tool_calls = message.tool_calls

        messages.append(message)

        # TODO: Create an AgentStep and log tool call records
        tool_records = []

        if content:
            logger.info(f"[Step {step + 1}] {content[:200]}")

        if tool_calls:
            for tc in tool_calls:
                func_name = tc.function.name
                func_args = json.loads(tc.function.arguments)
                args_str = json.dumps(func_args)

                logger.info(f"[Step {step + 1}] Tool: {func_name}({args_str})")

                # TODO: Check for loops BEFORE executing
                # loop_check = loop_detector.check_tool_call(func_name, args_str)
                # if loop_check.is_looping:
                #     # Inject warning instead of executing
                #     messages.append({
                #         "tool_call_id": tc.id,
                #         "role": "tool",
                #         "name": func_name,
                #         "content": f"LOOP DETECTED: {loop_check.message}",
                #     })
                #     continue

                # Execute tool (no loop detection = BUG)
                tool_start = time.time()
                result = TOOLS.get(func_name, lambda **_: "Unknown tool")(**func_args)
                tool_duration = (time.time() - tool_start) * 1000

                logger.info(f"[Step {step + 1}] Result: {result[:150]}")

                messages.append({
                    "tool_call_id": tc.id,
                    "role": "tool",
                    "name": func_name,
                    "content": result,
                })

        step_log.append({
            "step": step + 1,
            "content": content,
            "tool_calls": [
                {"name": tc.function.name, "args": tc.function.arguments}
                for tc in (tool_calls or [])
            ],
        })

        # TODO: Log the step to the tracer
        # step_duration = (time.time() - step_start) * 1000
        # agent_step = AgentStep(
        #     step_number=step + 1,
        #     reasoning=content,
        #     tool_calls=tool_records,
        #     duration_ms=step_duration,
        # )
        # tracer.log_step(trace_id, agent_step)

        if not tool_calls and content:
            # TODO: End the trace
            # tracer.end_trace(trace_id, content, status="completed")
            # tracer.print_summary(trace_id)
            return {
                "answer": content,
                "steps": step_log,
                "total_steps": step + 1,
            }

    # TODO: End trace with "max_steps_exceeded" status
    # tracer.end_trace(trace_id, "[Max steps reached]", status="failed",
    #                  error="Max steps exceeded")
    # tracer.print_summary(trace_id)
    return {
        "answer": "[Max steps reached — agent likely stuck in a loop]",
        "steps": step_log,
        "total_steps": max_steps,
    }


if __name__ == "__main__":
    print("=" * 60)
    print("Test 1: Query that works fine")
    print("=" * 60)
    result = run_broken_agent("What is the capital of France?")
    print(f"\nAnswer: {result['answer'][:200]}")
    print(f"Steps: {result['total_steps']}")

    print("\n" + "=" * 60)
    print("Test 2: Query that triggers infinite loop (BUG!)")
    print("=" * 60)
    result = run_broken_agent(
        "What are the latest trends in quantum computing?",
        max_steps=6,  # Limited to avoid burning tokens
    )
    print(f"\nAnswer: {result['answer'][:200]}")
    print(f"Steps: {result['total_steps']}")
