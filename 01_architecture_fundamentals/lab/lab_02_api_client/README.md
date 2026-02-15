# Lab 2: Building a Production-Grade API Client

## Overview
In this lab you will progressively build a robust Hugging Face API client — from a simple "hello world" request to a cached, retry-aware production pattern.

## Prerequisites
- Python 3.10+
- A free Hugging Face account with an API token ([huggingface.co/settings/tokens](https://huggingface.co/settings/tokens))
- Completion of Session 2 slides (API landscape, security)

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# Edit .env and paste your Hugging Face token
```

## 5-Step Progression

### Step 1: Security First
Open `starter/hello_hf.py`. The `.env` loading and `get_api_token()` function are provided. Read through them — understand *why* we never hardcode tokens.

### Step 2: Hello World
In the same file, complete the **TODO** to make a raw `requests.post` call to the Hugging Face Inference API. Run the script and confirm you get a generated response.

```bash
python starter/hello_hf.py
```

### Step 3: The Wrapper Class
Open `starter/hf_client.py`. The `HuggingFaceClient` class skeleton is provided with `__init__` complete. The helper functions (`text_generation`, `summarization`, `text_classification`) are also provided. Your job is to implement the `query()` method with error handling.

### Step 4: Resilience
Still in `hf_client.py`, complete the three **TODO** blocks inside `query()`:
1. Handle **503** (model loading / cold start) — wait the estimated time, then retry
2. Handle **429** (rate limit) — exponential backoff
3. Handle **timeout** — retry with delay

### Step 5: Caching
Open `starter/cached_client.py`. Cache directory setup and key generation are provided. Complete the **TODO** blocks to:
1. Check if a cached response exists
2. Write new responses to cache
3. Return cached responses on hit

```bash
python starter/cached_client.py
# Run it twice — the second run should show "[Cache HIT]"
```

## Checking Your Work
Compare your implementations against the files in `solutions/`. The solution files are complete, working versions.

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `EnvironmentError: HUGGINGFACE_API_TOKEN not found` | Copy `.env.example` to `.env` and add your token |
| `401 Unauthorized` | Token may be expired — generate a new one on HF |
| `503 Model loading` | Normal on free tier — the retry logic handles this |
| `ModuleNotFoundError: dotenv` | Run `pip install -r requirements.txt` |
