from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

import os
from openai import OpenAI

from config import (
    SYSTEM_PROMPT,
    OPENAI_API_KEY, OPENAI_BASE_URL, OPENAI_MODEL,
    LLM_TEMPERATURE, LLM_MAX_TOKENS,
    OPENROUTER_SITE_URL, OPENROUTER_APP_NAME,
)

# Prépare les headers recommandés par OpenRouter
default_headers = {}
if OPENROUTER_SITE_URL:
    default_headers["HTTP-Referer"] = OPENROUTER_SITE_URL
if OPENROUTER_APP_NAME:
    default_headers["X-Title"] = OPENROUTER_APP_NAME

# Client OpenAI-compatible pointant sur OpenRouter
client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL,        # https://openrouter.ai/api/v1
    default_headers=default_headers or None,
)

def generate_response(prompt: str) -> str:
    try:
        resp = client.chat.completions.create(
            model=OPENAI_MODEL,       # ex: meta-llama/llama-3.1-8b-instruct:free
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": prompt},
            ],
            temperature=LLM_TEMPERATURE,
            max_tokens=LLM_MAX_TOKENS,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        print(f"[LLM] Error: {e}")
        return "Désolé, j'ai rencontré un problème pour répondre."