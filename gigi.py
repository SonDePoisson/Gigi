"""
gigi.py
----------------------------
Continuously listens to the microphone and transcribes speech in real-time
using OpenAI Whisper (Hugging Face Transformers) in French.
"""

import time
from typing import Any
import numpy as np
import torch
import speech_recognition as sr
from transformers import pipeline
from functools import partial

SAMPLE_RATE: int = 16000
WHISPER_MODEL: str = "openai/whisper-small"
LANGUAGE: str = "fr"


def audio_callback(
    asr_pipeline: Any, recognizer: sr.Recognizer, audio: sr.AudioData
) -> None:
    """
    Callback to transcribe audio chunks using Whisper.
    """
    try:
        raw_data = audio.get_raw_data(convert_rate=SAMPLE_RATE, convert_width=2)
        audio_np = np.frombuffer(raw_data, np.int16).astype(np.float32) / 32768.0
        result = asr_pipeline(audio_np)
        text = result.get("text", "").strip()
        if text:
            print(f"User: {text}")
    except Exception as e:
        print(f"Error: {e}")


def main():
    # Select device
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")

    asr_pipeline: Any = pipeline(
        task="automatic-speech-recognition",
        model=WHISPER_MODEL,
        device=device,
        generate_kwargs={"task": "transcribe", "language": LANGUAGE},
    )

    recognizer = sr.Recognizer()
    mic = sr.Microphone(sample_rate=SAMPLE_RATE)

    print("Listening... Press Ctrl+C to stop.")

    # Use partial to pass asr_pipeline to callback
    callback_with_pipeline = partial(audio_callback, asr_pipeline)
    stop_listening = recognizer.listen_in_background(mic, callback_with_pipeline)

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        stop_listening(wait_for_stop=False)
        print("Listening stopped.")


if __name__ == "__main__":
    main()
