"""
Lab 2 - Steps 2 & 3: Multi-Agent Orchestrator
================================================
Build a MultiAgentOrchestrator that coordinates specialists
through a 4-phase workflow: Research -> Analysis -> Writing -> Quality Gate.
"""

import asyncio
import logging
from specialists import create_researcher, create_analyst, create_writer, call_agent

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)


class SharedWorkspace:
    """Simple shared state between agents — stores entries by type."""

    def __init__(self):
        self.entries = []

    def write(self, author: str, content: str, entry_type: str):
        """Add an entry to the workspace."""
        self.entries.append({
            "author": author,
            "type": entry_type,
            "content": content,
        })

    def read_all(self) -> str:
        """Read all entries as a formatted string."""
        parts = []
        for entry in self.entries:
            parts.append(
                f"[{entry['author'].upper()} - {entry['type']}]\n{entry['content']}"
            )
        return "\n\n---\n\n".join(parts)

    def read_by_type(self, entry_type: str) -> list[str]:
        """Read entries of a specific type."""
        return [e["content"] for e in self.entries if e["type"] == entry_type]


class MultiAgentOrchestrator:
    """
    Coordinates a team of specialist agents.

    Workflow:
    1. Research (parallel if multi-topic)
    2. Analysis
    3. Writing
    4. Quality Gate (review loop)
    """

    def __init__(self, max_revisions: int = 2):
        self.researcher = create_researcher()
        self.analyst = create_analyst()
        self.writer = create_writer()
        self.max_revisions = max_revisions
        self.workspace = SharedWorkspace()

    async def run(self, query: str) -> dict:
        """Execute the full multi-agent workflow."""
        self.workspace = SharedWorkspace()

        # Phase 1: Research
        research_tasks = self._plan_research(query)
        logger.info(f"[Orchestrator] Phase 1: {len(research_tasks)} research task(s)")

        # TODO: Execute research tasks
        # If there are multiple tasks, run them in parallel with asyncio.gather
        # If there's only one task, run it directly
        # Hint for parallel: Use asyncio.get_event_loop().run_in_executor()
        #   to wrap the synchronous call_agent() in an async context

        # --- YOUR CODE HERE ---
        research_results = []  # Replace: should contain research results
        # --- END YOUR CODE ---

        # Store research results in workspace
        for result in research_results:
            self.workspace.write(
                author="researcher",
                content=result,
                entry_type="research",
            )

        # Phase 2: Analysis
        logger.info(f"[Orchestrator] Phase 2: Analysis")
        research_context = self.workspace.read_all()

        # TODO: Run the analyst on the research findings
        # Hint: call_agent(self.analyst, f"Analyze these findings for: {query}\n\n{research_context}")

        # --- YOUR CODE HERE ---
        analysis_result = ""  # Replace this
        # --- END YOUR CODE ---

        self.workspace.write(
            author="analyst",
            content=analysis_result,
            entry_type="analysis",
        )

        # Phase 3: Writing
        logger.info(f"[Orchestrator] Phase 3: Writing")
        full_context = self.workspace.read_all()

        # TODO: Run the writer to produce a draft
        # Hint: call_agent(self.writer, f"Write a report for: {query}\n\n{full_context}")

        # --- YOUR CODE HERE ---
        draft = ""  # Replace this
        # --- END YOUR CODE ---

        self.workspace.write(
            author="writer",
            content=draft,
            entry_type="draft",
        )

        # Phase 4: Quality Gate
        final_output = await self._quality_gate(query, draft)

        return {
            "output": final_output,
            "workspace_entries": len(self.workspace.entries),
            "revision_count": len(self.workspace.read_by_type("revision_note")),
        }

    def _plan_research(self, query: str) -> list[str]:
        """
        Split a query into parallel research tasks if it involves comparison.
        Returns a list of research instructions.
        """
        query_lower = query.lower()

        # Check for comparison patterns
        for separator in [" versus ", " vs ", " vs. ", " and "]:
            if separator in query_lower and any(
                kw in query_lower for kw in ["compare", "versus", "vs"]
            ):
                parts = query.split(separator)
                if len(parts) >= 2:
                    return [
                        f"Research the following topic thoroughly: {part.strip()}"
                        for part in parts
                    ]

        # Default: single research task
        return [f"Research the following topic thoroughly: {query}"]

    async def _quality_gate(self, query: str, draft: str) -> str:
        """
        Have the Analyst review the draft. If issues found, send
        revision notes back to the Writer.

        TODO: Implement the review loop:
        1. Ask the Analyst to review the draft
        2. If Analyst says "APPROVED", return the draft
        3. Otherwise, send revision notes to Writer for a revised draft
        4. Repeat up to max_revisions times
        """

        # --- YOUR CODE HERE ---
        # Hint: Loop max_revisions times. In each iteration:
        #   review = call_agent(self.analyst, f"Review this draft... If acceptable: APPROVED")
        #   if "APPROVED" in review.upper(): return current_draft
        #   else: current_draft = call_agent(self.writer, f"Revise based on: {review}")
        return draft  # Replace: should go through quality gate
        # --- END YOUR CODE ---


async def main():
    orchestrator = MultiAgentOrchestrator()
    result = await orchestrator.run(
        "Compare the environmental policies of the EU and US, "
        "evaluate their effectiveness, and write an executive briefing"
    )
    print("\n" + "=" * 60)
    print("FINAL OUTPUT:")
    print("=" * 60)
    print(result["output"])
    print(f"\nWorkspace entries: {result['workspace_entries']}")
    print(f"Revisions: {result['revision_count']}")


if __name__ == "__main__":
    asyncio.run(main())
