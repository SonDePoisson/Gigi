from config import ENV_PATH
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs.play import play
import os
from gtts import gTTS
import tempfile
import playsound


def init_tts(TTS: str = None) -> ElevenLabs | None:
    if TTS == "Eleven":
        load_dotenv(ENV_PATH)
        elevenlabs = ElevenLabs(
            api_key=os.getenv("ELEVENLABS_API_KEY"),
        )
        print("[TTS] : ElevenLabs")
    else:
        elevenlabs = None
        print("[TTS] : gTTS")
    return elevenlabs


def speak(
    text: str, elevenlabs: ElevenLabs | None, voice: str = None, model: str = None
):
    if elevenlabs is None:
        tts = gTTS(text=text, lang="fr")

        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
            tts.save(f.name)
            path = f.name

        playsound.playsound(path, block=True)
    else:
        audio = elevenlabs.text_to_speech.convert(
            text=text,
            voice_id=voice,
            model_id=model,
            output_format="mp3_44100_128",
        )
        play(audio)
