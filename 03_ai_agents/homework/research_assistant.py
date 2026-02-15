"""
Homework: The Autonomous Research Assistant
=============================================
A CLI tool that uses multi-agent orchestration with full tracing
to research a topic and produce a verified report.

Usage:
    python research_assistant.py "Your research query here"

Prerequisites:
    pip install -r requirements.txt
    Set OPENAI_API_KEY in .env file
"""

import os
import sys
import json
import time
import uuid
import asyncio
import logging
from dataclasses import dataclass, field, asdict
from typing import Optional
from dotenv import load_dotenv
from litellm import completion

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)

load_dotenv()
MODEL = os.getenv("MODEL_NAME", "gpt-4o")


# =============================================================================
# Tracer (copy from Lab 3 or project/src/observability/tracer.py)
# =============================================================================

@dataclass
class ToolCallRecord:
    tool_name: str
    tool_input: dict
    tool_output: str
    duration_ms: float


@dataclass
class AgentStep:
    step_number: int
    reasoning: Optional[str]
    tool_calls: list[ToolCallRecord] = field(default_factory=list)
    cost_usd: float = 0.0
    duration_ms: float = 0.0


@dataclass
class Trace:
    trace_id: str
    agent_name: str
    input_query: str
    model: str = ""
    steps: list[AgentStep] = field(default_factory=list)
    final_output: Optional[str] = None
    total_cost_usd: float = 0.0
    total_duration_ms: float = 0.0
    status: str = "running"


# TODO: Implement the AgentTracer class (or copy from Lab 3)
# class AgentTracer:
#     ...


# =============================================================================
# Loop Detector (copy from Lab 3 or project/src/observability/loop_detector.py)
# =============================================================================

# TODO: Implement the AdvancedLoopDetector class (or copy from Lab 3)
# class AdvancedLoopDetector:
#     ...


# =============================================================================
# Specialist Agents
# =============================================================================

# HINT: You may need to modify this function to return more than just the content string
# (e.g., token usage, cost) if you want to support the AgentTracer fully.
def call_agent(agent: dict, task: str) -> str:
    """Run a single-turn agent call."""
    response = completion(
        model=agent["model"],
        messages=[
            {"role": "system", "content": agent["system_prompt"]},
            {"role": "user", "content": task},
        ],
        max_tokens=1024,
    )
    return response.choices[0].message.content


def create_researcher(model: str = None) -> dict:
    """The Researcher: finds and retrieves information."""
    return {
        "name": "researcher",
        "system_prompt": (
            "You are a Research Specialist. Your ONLY job is to find and retrieve "
            "relevant information. Always cite sources. Return raw findings organized "
            "by source. Do NOT analyze or summarize."
        ),
        "model": model or MODEL,
    }


def create_analyst(model: str = None) -> dict:
    """The Analyst: evaluates and cross-references."""
    return {
        "name": "analyst",
        "system_prompt": (
            "You are an Analysis Specialist. Evaluate information, cross-reference "
            "claims, flag contradictions, identify gaps. Rate confidence: High/Medium/Low."
        ),
        "model": model or MODEL,
    }


def create_writer(model: str = None) -> dict:
    """The Writer: synthesizes into polished output."""
    return {
        "name": "writer",
        "system_prompt": (
            "You are a Writing Specialist. Produce clear, well-structured documents "
            "from analyzed research. Preserve citations. Include confidence qualifiers. "
            "Be concise."
        ),
        "model": model or MODEL,
    }


# =============================================================================
# Traced Multi-Agent Orchestrator
# =============================================================================

class TracedOrchestrator:
    """
    Multi-agent orchestrator with full tracing support.

    TODO: Implement this class by combining:
    1. Multi-agent workflow (Research -> Analysis -> Writing -> Quality Gate)
    2. AgentTracer for logging every phase
    3. AdvancedLoopDetector for error handling (optional for basic version)

    Phases:
    1. Research - gather information (parallel for multi-topic queries)
    2. Analysis - evaluate and cross-reference findings
    3. Writing - produce a polished report
    4. Quality Gate - Analyst reviews, Writer revises if needed
    """

    def __init__(self, max_revisions: int = 2):
        self.researcher = create_researcher()
        self.analyst = create_analyst()
        self.writer = create_writer()
        self.max_revisions = max_revisions
        # TODO: Initialize AgentTracer
        # self.tracer = AgentTracer(verbose=True)

    async def run(self, query: str) -> dict:
        """
        Execute the traced multi-agent workflow.

        TODO:
        1. Start a trace
        2. Run Phase 1: Research (parallel if multi-topic)
        3. Run Phase 2: Analysis
        4. Run Phase 3: Writing
        5. Run Phase 4: Quality Gate
        6. End the trace
        7. Print the trace summary
        8. Return the final output with trace info
        """
        start_time = time.time()

        # TODO: Start trace
        # trace_id = self.tracer.start_trace("research_assistant", query, MODEL)

        # Phase 1: Research
        logger.info(f"[Phase 1] Researching: {query[:60]}...")
        research_result = call_agent(
            self.researcher,
            f"Research the following topic thoroughly: {query}"
        )

        # Phase 2: Analysis
        logger.info(f"[Phase 2] Analyzing findings...")
        analysis_result = call_agent(
            self.analyst,
            f"Analyze these research findings for: {query}\n\n{research_result}"
        )

        # Phase 3: Writing
        logger.info(f"[Phase 3] Writing report...")
        draft = call_agent(
            self.writer,
            f"Write a polished report for: {query}\n\n"
            f"Research:\n{research_result}\n\nAnalysis:\n{analysis_result}"
        )

        # Phase 4: Quality Gate
        logger.info(f"[Phase 4] Quality review...")
        final_output = self._quality_gate(query, draft)

        duration = (time.time() - start_time) * 1000

        # TODO: End trace and print summary
        # self.tracer.end_trace(trace_id, final_output, status="completed")
        # self.tracer.print_summary(trace_id)

        return {
            "query": query,
            "output": final_output,
            "duration_ms": round(duration, 0),
        }

    def _quality_gate(self, query: str, draft: str) -> str:
        """Analyst reviews draft; Writer revises if needed."""
        current_draft = draft

        for revision in range(self.max_revisions):
            review = call_agent(
                self.analyst,
                f"Review this draft for: {query}\n\n"
                f"Draft:\n{current_draft}\n\n"
                f"If acceptable, respond with: APPROVED\n"
                f"Otherwise, provide revision instructions."
            )

            if "APPROVED" in review.upper():
                logger.info(f"  [Quality Gate] Approved after {revision} revision(s)")
                return current_draft

            logger.info(f"  [Quality Gate] Revision {revision + 1} requested")
            current_draft = call_agent(
                self.writer,
                f"Revise based on feedback:\n\n"
                f"Query: {query}\nDraft:\n{current_draft}\nFeedback:\n{review}"
            )

        return current_draft


# =============================================================================
# CLI Entry Point
# =============================================================================

async def main():
    if len(sys.argv) < 2:
        print("Usage: python research_assistant.py \"Your research query\"")
        print("\nExample:")
        print('  python research_assistant.py "Compare Python and Rust for systems programming"')
        sys.exit(1)

    query = " ".join(sys.argv[1:])

    print("=" * 60)
    print("AUTONOMOUS RESEARCH ASSISTANT")
    print("=" * 60)
    print(f"Query: {query}")
    print(f"Model: {MODEL}")
    print("=" * 60)

    orchestrator = TracedOrchestrator()
    result = await orchestrator.run(query)

    print("\n" + "=" * 60)
    print("FINAL REPORT")
    print("=" * 60)
    print(result["output"])
    print("\n" + "=" * 60)
    print(f"Completed in {result['duration_ms']:.0f}ms")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
