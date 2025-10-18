from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parent / ".env")

import os
from openai import OpenAI

API_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = os.getenv("OPENAI_BASE_URL")
MODEL = os.getenv("OPENAI_MODEL", "meta-llama/llama-3.1-8b-instruct:free")

headers = {}
if os.getenv("OPENROUTER_SITE_URL"):
    headers["HTTP-Referer"] = os.getenv("OPENROUTER_SITE_URL")
if os.getenv("OPENROUTER_APP_NAME"):
    headers["X-Title"] = os.getenv("OPENROUTER_APP_NAME")

print("Key prefix :", (API_KEY or "")[:5] + "...")
print("Base URL   :", BASE_URL)
print("Model      :", MODEL)

client = OpenAI(api_key=API_KEY, base_url=BASE_URL, default_headers=headers or None)

resp = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role":"system","content":"Parle français, phrase courte."},
        {"role":"user","content":"Explique en une phrase le but du jeu Odin."}
    ],
    max_tokens=80,
    temperature=0.5,
)
print("Réponse :", resp.choices[0].message.content)