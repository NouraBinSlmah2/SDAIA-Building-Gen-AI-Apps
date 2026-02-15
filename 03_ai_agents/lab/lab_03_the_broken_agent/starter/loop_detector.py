"""
Lab 3 - Step 2: Advanced Loop Detector
========================================
Detects agent loops using three strategies:
1. Exact Match — same tool + same arguments repeated
2. Fuzzy Match — similar arguments (Jaccard similarity)
3. Output Stagnation — agent outputs are too similar
"""

from dataclasses import dataclass


@dataclass
class LoopDetectionResult:
    """Result of a loop check."""
    is_looping: bool
    strategy: str   # "exact", "fuzzy", "stagnation", "none"
    message: str
    confidence: float  # 0.0 to 1.0


class AdvancedLoopDetector:
    """
    Detects agent loops using three strategies.

    TODO: Implement these methods:
    1. _jaccard_similarity() - word-level Jaccard similarity
    2. check_tool_call() - check for exact and fuzzy loops
    3. check_output_stagnation() - check for repetitive outputs
    """

    def __init__(
        self,
        exact_threshold: int = 2,       # Trigger after 2 exact repeats
        fuzzy_threshold: float = 0.8,    # Jaccard similarity threshold
        stagnation_window: int = 3,      # Check last N outputs
    ):
        self.exact_threshold = exact_threshold
        self.fuzzy_threshold = fuzzy_threshold
        self.stagnation_window = stagnation_window

        self.tool_history: list[tuple[str, str]] = []   # (tool_name, args_str)
        self.output_history: list[str] = []

    def _jaccard_similarity(self, s1: str, s2: str) -> float:
        """
        Compute Jaccard similarity between two strings using word-level tokens.

        Jaccard = |intersection| / |union|

        TODO:
        1. Split both strings into lowercase word sets
        2. Compute intersection and union
        3. Return |intersection| / |union|
        4. Handle edge cases (empty strings)
        """
        # --- YOUR CODE HERE ---
        return 0.0
        # --- END YOUR CODE ---

    def check_tool_call(
        self, tool_name: str, tool_input: str
    ) -> LoopDetectionResult:
        """
        Check if a tool call indicates a loop. Call BEFORE executing the tool.

        TODO:
        1. Strategy 1 (Exact Match):
           - Count how many times (tool_name, tool_input) appears in history
           - If count >= exact_threshold, return is_looping=True, strategy="exact"

        2. Strategy 2 (Fuzzy Match):
           - Check last 5 calls for same tool_name with similar arguments
           - Use _jaccard_similarity; if similarity >= fuzzy_threshold, count it
           - If fuzzy_matches >= exact_threshold, return is_looping=True, strategy="fuzzy"

        3. Always append current call to history before returning
        """
        current = (tool_name, tool_input.strip())

        # --- YOUR CODE HERE ---
        # Strategy 1: Exact Match

        # Strategy 2: Fuzzy Match

        # --- END YOUR CODE ---

        self.tool_history.append(current)
        return LoopDetectionResult(
            is_looping=False, strategy="none", message="", confidence=0.0
        )

    def check_output_stagnation(self, output: str) -> LoopDetectionResult:
        """
        Check if the agent's outputs are stagnating.

        TODO:
        1. Append output to history
        2. If we have fewer than stagnation_window outputs, return not looping
        3. Get the last stagnation_window outputs
        4. Compute pairwise Jaccard similarity
        5. If average similarity >= fuzzy_threshold, return is_looping=True
        """
        # --- YOUR CODE HERE ---
        self.output_history.append(output)
        return LoopDetectionResult(
            is_looping=False, strategy="none", message="", confidence=0.0
        )
        # --- END YOUR CODE ---

    def reset(self):
        """Reset detector state for a new query."""
        self.tool_history.clear()
        self.output_history.clear()


if __name__ == "__main__":
    detector = AdvancedLoopDetector()

    # Test exact match detection
    print("=== Exact Match Test ===")
    r1 = detector.check_tool_call("search", '{"query": "python tutorial"}')
    print(f"Call 1: {r1}")
    r2 = detector.check_tool_call("search", '{"query": "python tutorial"}')
    print(f"Call 2: {r2}")
    r3 = detector.check_tool_call("search", '{"query": "python tutorial"}')
    print(f"Call 3 (should detect loop): {r3}")

    # Test fuzzy match detection
    print("\n=== Fuzzy Match Test ===")
    detector.reset()
    detector.check_tool_call("search", "python tutorial basics")
    detector.check_tool_call("search", "basics python tutorial")
    r = detector.check_tool_call("search", "tutorial python basics")
    print(f"Fuzzy (should detect): {r}")

    # Test Jaccard similarity
    print("\n=== Jaccard Similarity Test ===")
    sim = detector._jaccard_similarity("python tutorial basics", "basics python tutorial")
    print(f"Jaccard('python tutorial basics', 'basics python tutorial') = {sim}")
