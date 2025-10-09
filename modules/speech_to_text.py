import numpy as np
import torch
from transformers import pipeline
from config import WHISPER_MODEL, LANGUAGE, SAMPLE_RATE

device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
asr_pipeline = pipeline(
    task="automatic-speech-recognition",
    model=WHISPER_MODEL,
    device=device,
    generate_kwargs={"task": "transcribe", "language": LANGUAGE},
)


def transcribe_audio(audio):
    raw_data = audio.get_raw_data(convert_rate=SAMPLE_RATE, convert_width=2)
    audio_np = np.frombuffer(raw_data, np.int16).astype(np.float32) / 32768.0
    result = asr_pipeline(audio_np)
    return result.get("text", "").strip()
