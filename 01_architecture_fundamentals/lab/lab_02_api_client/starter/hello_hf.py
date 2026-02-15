"""
Lab 2 — Steps 1 & 2: Environment Setup + First API Call

Step 1: Read through the get_api_token() function — understand why we
        never hardcode tokens.
Step 2: Complete the TODO at the bottom to make your first API call.
"""

import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_api_token():
    """Retrieve API token with validation."""
    token = os.getenv("HUGGINGFACE_API_TOKEN")
    if not token:
        raise EnvironmentError(
            "HUGGINGFACE_API_TOKEN not found. "
            "Create a .env file with your token or set the environment variable."
        )
    if not token.startswith("hf_"):
        raise ValueError(
            "Invalid Hugging Face token format. Token should start with 'hf_'."
        )
    return token


# --- Configuration ---
API_URL = "https://api-inference.huggingface.co/models/"
MODEL_ID = "mistralai/Mistral-7B-Instruct-v0.3"
TOKEN = get_api_token()
HEADERS = {"Authorization": f"Bearer {TOKEN}"}


# =====================================================================
# TODO (Step 2): Make your first API call
#
# Use requests.post() to send a request to the Hugging Face Inference API.
#
# Hints:
#   - URL: f"{API_URL}{MODEL_ID}"
#   - Pass `headers=HEADERS`
#   - Pass a JSON body: {"inputs": prompt, "parameters": {...}}
#   - Key parameters: max_new_tokens=150, temperature=0.7, return_full_text=False
#   - Call response.raise_for_status() to catch HTTP errors
#   - Parse with response.json()
#   - The generated text is at result[0]["generated_text"]
# =====================================================================

prompt = "Explain what a vector database is in one paragraph:"

# Your code here:
# response = requests.post(...)
# response.raise_for_status()
# result = response.json()
# print("Generated Text:")
# print(result[0]["generated_text"])
