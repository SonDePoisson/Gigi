from TTS.api import TTS
import torch
import tempfile
import playsound
import soundfile as sf
from config import COQUI_MODEL


def init_tts():
    tts = TTS(model_name=COQUI_MODEL, gpu=torch.cuda.is_available())
    return tts


def speak(text: str, tts: TTS):
    wav = tts.tts(text)

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        sf.write(f.name, wav, samplerate=tts.synthesizer.output_sample_rate)
        path = f.name

    playsound.playsound(path, block=True)
