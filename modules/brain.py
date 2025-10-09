from ollama import chat
from config import OLLAMA_MODEL, SYSTEM_PROMPT


def generate_response(prompt: str) -> str:
    try:
        response = chat(
            model=OLLAMA_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            options={"temperature": 0.7},
        )
        return response["message"]["content"].strip()
    except Exception as e:
        print(f"Error while generating response: {e}")
        return "Désolé, j'ai rencontré un problème pour répondre."
