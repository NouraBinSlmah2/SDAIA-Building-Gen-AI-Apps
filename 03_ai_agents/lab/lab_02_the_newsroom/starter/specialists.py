"""
Lab 2 - Step 1: Specialist Agents for the Newsroom
====================================================
Create three specialist agents with focused roles.

Each specialist is a simple dict with:
  - "name": the agent's role name
  - "system_prompt": constrains the agent to its role
  - "model": the LLM model to use
  - "max_steps": max reasoning steps (specialists finish fast)
"""

import os
import json
from dotenv import load_dotenv
from litellm import completion

load_dotenv()
MODEL = os.getenv("MODEL_NAME", "gpt-4o")


def call_agent(agent: dict, task: str) -> str:
    """
    Run a simple agent loop: call the LLM, return the response.
    For this lab, specialists are single-turn (no tool calling).
    They receive context and produce output in one pass.
    """
    messages = [
        {"role": "system", "content": agent["system_prompt"]},
        {"role": "user", "content": task},
    ]

    response = completion(
        model=agent["model"],
        messages=messages,
        max_tokens=1024,
    )

    return response.choices[0].message.content


def create_researcher(model: str = None) -> dict:
    """
    The Researcher: finds and retrieves relevant information.

    TODO: Define a system prompt that:
    - Constrains the agent to ONLY find and retrieve information
    - Requires citing sources
    - Forbids analysis or summarization
    - Returns raw findings organized by source

    Returns:
        dict with keys: name, system_prompt, model, max_steps
    """
    # TODO: Write the researcher system prompt
    system_prompt = """
    # --- YOUR CODE HERE ---
    # Write a system prompt for the Researcher specialist.
    # Hint: Tell it to ONLY research, cite sources, and return raw findings.
    # --- END YOUR CODE ---
    """

    return {
        "name": "researcher",
        "system_prompt": system_prompt,
        "model": model or MODEL,
        "max_steps": 8,
    }


def create_analyst(model: str = None) -> dict:
    """
    The Analyst: evaluates, cross-references, and identifies patterns.

    TODO: Define a system prompt that:
    - Constrains the agent to ONLY analyze provided information
    - Requires cross-referencing claims across sources
    - Flags contradictions explicitly
    - Rates confidence: High / Medium / Low
    - Identifies gaps in the research

    Returns:
        dict with keys: name, system_prompt, model, max_steps
    """
    # TODO: Write the analyst system prompt
    system_prompt = """
    # --- YOUR CODE HERE ---
    # Write a system prompt for the Analyst specialist.
    # Hint: Tell it to evaluate info, flag contradictions, rate confidence.
    # --- END YOUR CODE ---
    """

    return {
        "name": "analyst",
        "system_prompt": system_prompt,
        "model": model or MODEL,
        "max_steps": 6,
    }


def create_writer(model: str = None) -> dict:
    """
    The Writer: synthesizes analysis into polished, readable output.

    TODO: Define a system prompt that:
    - Constrains the agent to ONLY write from provided context
    - Requires clear structure (headings, transitions)
    - Preserves citations from research
    - Includes confidence qualifiers from analysis
    - Keeps output concise

    Returns:
        dict with keys: name, system_prompt, model, max_steps
    """
    # TODO: Write the writer system prompt
    system_prompt = """
    # --- YOUR CODE HERE ---
    # Write a system prompt for the Writer specialist.
    # Hint: Tell it to write clearly, preserve citations, be concise.
    # --- END YOUR CODE ---
    """

    return {
        "name": "writer",
        "system_prompt": system_prompt,
        "model": model or MODEL,
        "max_steps": 4,
    }


if __name__ == "__main__":
    # Quick test: each specialist should respond in character
    researcher = create_researcher()
    analyst = create_analyst()
    writer = create_writer()

    print("=== Researcher ===")
    print(f"Name: {researcher['name']}")
    print(f"Prompt preview: {researcher['system_prompt'][:100]}...")

    print("\n=== Analyst ===")
    print(f"Name: {analyst['name']}")
    print(f"Prompt preview: {analyst['system_prompt'][:100]}...")

    print("\n=== Writer ===")
    print(f"Name: {writer['name']}")
    print(f"Prompt preview: {writer['system_prompt'][:100]}...")
