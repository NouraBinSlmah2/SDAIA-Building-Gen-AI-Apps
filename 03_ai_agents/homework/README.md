# Homework: The Autonomous Research Assistant

## Overview

Build a CLI tool that takes a complex user query, plans a research strategy, executes it using a multi-agent team, and writes a verified report -- all with full tracing.

This capstone integrates everything from Module 03:
- **Session 1:** The ReAct agent loop (single-agent reasoning)
- **Session 2:** Multi-agent orchestration (specialists + orchestrator)
- **Session 3:** Tracing, loop detection, and evaluation

## Requirements

### Must Have
1. Use `MultiAgentOrchestrator` with Researcher, Analyst, and Writer specialists
2. Implement full `AgentTracer` support (every step logged)
3. Handle at least one "tool error" gracefully (circuit breaker or fallback)
4. Output a structured trace summary after each run

### Bonus
- Add a **Router** that classifies queries before assigning to specialists
- Run the agent against an eval dataset and report pass/fail rates
- Implement cost tracking with per-query budget limits

## Getting Started

1. Copy or reference files from the project folder:
   - `project/src/agent/react_agent.py`
   - `project/src/agent/specialists.py`
   - `project/src/agent/multi_agent.py`
   - `project/src/observability/tracer.py`
   - `project/src/observability/loop_detector.py`

2. Complete the starter template: `research_assistant.py`

3. Run:
   ```bash
   pip install -r requirements.txt
   python research_assistant.py "Compare Python and Rust for systems programming"
   ```

## Starter Template

The `research_assistant.py` file provides:
- CLI argument parsing
- Skeleton for `TracedOrchestrator` class
- TODOs for integrating tracing, loop detection, and the multi-agent workflow

## Evaluation Criteria

| Criterion | Weight |
|:----------|:-------|
| Multi-agent workflow works end-to-end | 30% |
| Full tracing with readable summaries | 25% |
| Graceful error/loop handling | 25% |
| Code quality and documentation | 20% |

## Time Estimate

2-3 hours for core requirements. Bonus tasks add 1-2 hours.
