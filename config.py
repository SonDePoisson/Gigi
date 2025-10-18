from pathlib import Path
from dotenv import load_dotenv
import os

ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(ENV_PATH)  # charge .env à côté de config.py, peu importe d'où tu lances


import os


SAMPLE_RATE = 16000
WHISPER_MODEL = "openai/whisper-large-v3"
COQUI_MODEL = "tts_models/fr/css10/vits"
WHISPER_MODEL = "openai/whisper-small"  # whisper-large-v3
LANGUAGE = "fr"
OLLAMA_MODEL = "llama3.1:8b"
BAD_PATTERNS = ["Sous-titres réalisés par la communauté d'Amara.org"]


# LLM (compatible OpenAI/OpenRouter)
OPENAI_API_KEY  = os.getenv("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", None)  # ← pour OpenRouter on met l’URL
OPENAI_MODEL    = os.getenv("OPENAI_MODEL", "meta-llama/llama-3.1-8b-instruct:free")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.5"))
LLM_MAX_TOKENS  = int(os.getenv("LLM_MAX_TOKENS", "300"))


'''
SYSTEM_PROMPT = (
    "Tu es un assistant vocal français. "
    "Réponds toujours en français, avec des phrases courtes et naturelles. "
    "Parle simplement."
)
'''

SYSTEM_PROMPT = (
    "Tu es Rùlia, assistant vocale **français** experte du jeu 'Odin' qui est le jeu de défausse qui se joue de 2 à 5 joueurs. "
    "Réponds en français en phrases courtes, claires et sûres. "
    "Priorité: expliquer le but, guider les 2 premiers tours, répondre aux questions de règles. "
    "Si une question sort des règles d'Odin, tu peux répondre mais guider ensuite la conversation vers le jeu Odin"
)

# Headers OpenRouter (facultatif mais utile)
OPENROUTER_SITE_URL = os.getenv("OPENROUTER_SITE_URL", None)
OPENROUTER_APP_NAME = os.getenv("OPENROUTER_APP_NAME", None)
