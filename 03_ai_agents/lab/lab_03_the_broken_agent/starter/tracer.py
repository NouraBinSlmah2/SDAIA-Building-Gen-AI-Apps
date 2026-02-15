"""
Lab 3 - Step 1: Agent Tracer
==============================
Build a structured tracer that captures every step of agent execution.
"""

import json
import time
import uuid
from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class ToolCallRecord:
    """Record of a single tool call within a step."""
    tool_name: str
    tool_input: dict
    tool_output: str
    duration_ms: float


@dataclass
class AgentStep:
    """A single step in the agent's execution."""
    step_number: int
    reasoning: Optional[str]
    tool_calls: list[ToolCallRecord] = field(default_factory=list)
    input_tokens: int = 0
    output_tokens: int = 0
    cost_usd: float = 0.0
    duration_ms: float = 0.0
    timestamp: float = field(default_factory=time.time)


@dataclass
class Trace:
    """Complete trace of an agent execution."""
    trace_id: str
    agent_name: str
    input_query: str
    model: str = ""
    steps: list[AgentStep] = field(default_factory=list)
    final_output: Optional[str] = None
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    total_cost_usd: float = 0.0
    total_duration_ms: float = 0.0
    status: str = "running"  # running, completed, failed, loop_detected
    error: Optional[str] = None


class AgentTracer:
    """
    Captures agent execution flow for debugging and analysis.

    TODO: Implement the following methods:
    1. start_trace() - create a new Trace and store it
    2. log_step() - add a step to the trace and accumulate totals
    3. end_trace() - finalize the trace with status and output
    4. get_trace_json() - export as JSON string
    5. print_summary() - human-readable summary
    """

    def __init__(self, verbose: bool = True):
        self._traces: dict[str, Trace] = {}
        self.verbose = verbose

    def start_trace(self, agent_name: str, query: str, model: str = "") -> str:
        """
        Start a new trace for an agent execution.

        TODO:
        1. Generate a short unique trace_id (hint: str(uuid.uuid4())[:8])
        2. Create a Trace object and store it in self._traces
        3. If verbose, print trace start info
        4. Return the trace_id

        Returns:
            str: The trace ID
        """
        # --- YOUR CODE HERE ---
        pass
        # --- END YOUR CODE ---

    def log_step(self, trace_id: str, step: AgentStep):
        """
        Log a completed step to the trace.

        TODO:
        1. Look up the trace by trace_id
        2. Append the step to trace.steps
        3. Accumulate totals (tokens, cost, duration)
        4. If verbose, print step info (reasoning preview, tool calls)
        """
        # --- YOUR CODE HERE ---
        pass
        # --- END YOUR CODE ---

    def end_trace(self, trace_id: str, output: str,
                  status: str = "completed", error: str = None):
        """
        Mark a trace as complete.

        TODO:
        1. Look up the trace
        2. Set final_output, status, and error
        3. If verbose, print summary (steps, tokens, cost, duration)
        """
        # --- YOUR CODE HERE ---
        pass
        # --- END YOUR CODE ---

    def get_trace(self, trace_id: str) -> Optional[Trace]:
        """Get a trace by ID."""
        return self._traces.get(trace_id)

    def get_trace_json(self, trace_id: str) -> str:
        """
        Export a trace as formatted JSON for debugging.

        TODO: Convert the Trace dataclass to a JSON string using asdict().
        """
        # --- YOUR CODE HERE ---
        return "{}"
        # --- END YOUR CODE ---

    def print_summary(self, trace_id: str):
        """
        Print a human-readable summary of a trace.

        TODO: Print:
        - Agent name, model, status
        - Query
        - Each step with duration, cost, and tools used
        - Total tokens, cost, and time
        - Answer preview
        """
        # --- YOUR CODE HERE ---
        print(f"print_summary not yet implemented for trace {trace_id}")
        # --- END YOUR CODE ---


if __name__ == "__main__":
    # Quick test
    tracer = AgentTracer()
    tid = tracer.start_trace("test_agent", "What is 2+2?", "gpt-4o")
    if tid:
        step = AgentStep(
            step_number=1,
            reasoning="I need to calculate 2+2",
            tool_calls=[ToolCallRecord("calculate", {"expr": "2+2"}, "4", 10.0)],
            cost_usd=0.001,
            duration_ms=150.0,
        )
        tracer.log_step(tid, step)
        tracer.end_trace(tid, "The answer is 4.")
        tracer.print_summary(tid)
        print("\nJSON:")
        print(tracer.get_trace_json(tid))
