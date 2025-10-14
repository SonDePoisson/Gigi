import numpy as np
from transformers import pipeline, Pipeline
from speech_recognition import AudioData
from config import WHISPER_MODEL, LANGUAGE, SAMPLE_RATE

import torch


def init_asr() -> Pipeline:
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    return pipeline(
        task="automatic-speech-recognition",
        model=WHISPER_MODEL,
        device=device,
        generate_kwargs={"task": "transcribe", "language": LANGUAGE},
    )


def transcribe(
    asr_pipeline: Pipeline, audio: AudioData, sample_rate: int = SAMPLE_RATE
):
    raw_data = audio.get_raw_data(convert_rate=sample_rate, convert_width=2)
    audio_np = np.frombuffer(raw_data, np.int16).astype(np.float32) / 32768.0
    result = asr_pipeline({"array": audio_np, "sampling_rate": sample_rate})
    return result.get("text", "").strip()
