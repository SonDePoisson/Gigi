"""
gigi.py
----------------------------
Continuously listens to the microphone and transcribes speech in real-time
using OpenAI Whisper (Hugging Face Transformers) in French,
and repeats it using pyttsx3.
"""

from typing import Any
import numpy as np
import torch
import speech_recognition as sr
from transformers import pipeline
import pyttsx3

SAMPLE_RATE = 16000
WHISPER_MODEL = "openai/whisper-small"
LANGUAGE = "fr"
BAD_PATTERNS = ["Sous-titres réalisés par la communauté d'Amara.org"]


def main():
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")

    # Whisper
    asr_pipeline: Any = pipeline(
        task="automatic-speech-recognition",
        model=WHISPER_MODEL,
        device=device,
        generate_kwargs={"task": "transcribe", "language": LANGUAGE},
    )

    # Coqui TTS
    tts_engine = pyttsx3.init()
    tts_engine.setProperty("rate", 150)
    tts_engine.setProperty("volume", 1.0)

    # SoundRecognition
    recognizer = sr.Recognizer()
    mic = sr.Microphone(sample_rate=SAMPLE_RATE)

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening... Press Ctrl+C to stop.")

        while True:
            try:
                # listen until silence
                recognizer.pause_threshold = 2.0
                print("[Listening]")
                audio = recognizer.listen(source)
                print("[Processing]")

                # Convert to numpy for Whisper
                raw_data = audio.get_raw_data(convert_rate=SAMPLE_RATE, convert_width=2)
                audio_np = (
                    np.frombuffer(raw_data, np.int16).astype(np.float32) / 32768.0
                )

                result = asr_pipeline(audio_np)
                text = result.get("text", "").strip()

                if text and all(bad not in text for bad in BAD_PATTERNS):
                    print(f"User: {text}")
                    print("[Repeating]")
                    tts_engine.say(text)
                    tts_engine.runAndWait()
            except KeyboardInterrupt:
                print("\nStopping listening.")
                break
            except Exception as e:
                print(f"Error: {e}")


if __name__ == "__main__":
    main()
