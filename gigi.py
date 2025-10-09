"""
gigi.py
----------------------------
Continuously listens to the microphone and transcribes speech in real-time
using OpenAI Whisper (Hugging Face Transformers) in French,
generates a response using Llama 3.1:8b (via Ollama),
and speaks it aloud using pyttsx3.
"""

from typing import Any
import numpy as np
import torch
import speech_recognition as sr
from transformers import pipeline
import pyttsx3
from ollama import chat


SAMPLE_RATE: int = 16000
WHISPER_MODEL: str = "openai/whisper-small"
LANGUAGE: str = "fr"
BAD_PATTERNS = ["Sous-titres réalisés par la communauté d'Amara.org"]
OLLAMA_MODEL: str = "llama3.1:8b"
SYSTEM_PROMPT: str = (
    "Tu es un assistant vocal français. "
    "Réponds toujours en français, avec des phrases courtes et naturelles. "
    "Parle simplement"
)


def generate_response(prompt: str) -> str:
    """
    Generate a response using the local Ollama Llama 3.1:8b model.
    """
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


def main():
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")

    # Whisper
    asr_pipeline: Any = pipeline(
        task="automatic-speech-recognition",
        model=WHISPER_MODEL,
        device=device,
        generate_kwargs={"task": "transcribe", "language": LANGUAGE},
    )

    # TTS (pyttsx3)
    tts_engine = pyttsx3.init()
    tts_engine.setProperty("rate", 150)
    tts_engine.setProperty("volume", 1.0)

    # Speech Recognition
    recognizer = sr.Recognizer()
    mic = sr.Microphone(sample_rate=SAMPLE_RATE)

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening... (press Ctrl+C to stop)")

        while True:
            try:
                # Listen until silence
                recognizer.pause_threshold = 2.0
                print("[Listening]")
                audio = recognizer.listen(source)
                print("[Processing]")

                # Convert to numpy for Whisper
                raw_data = audio.get_raw_data(convert_rate=SAMPLE_RATE, convert_width=2)
                audio_np = (
                    np.frombuffer(raw_data, np.int16).astype(np.float32) / 32768.0
                )

                # Transcription
                result = asr_pipeline(audio_np)
                text = result.get("text", "").strip()

                if text and all(bad not in text for bad in BAD_PATTERNS):
                    print(f"User: {text}")

                    print("[Thinking]")
                    answer = generate_response(text)
                    print(f"AI: {answer}")

                    print("[Speaking]")
                    for segment in answer.split(". "):
                        if segment.strip():
                            tts_engine.say(segment.strip())
                            tts_engine.runAndWait()

            except KeyboardInterrupt:
                print("\nListening stopped.")
                break
            except Exception as e:
                print(f"Error: {e}")


if __name__ == "__main__":
    main()
