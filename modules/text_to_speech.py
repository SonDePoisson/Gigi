from config import ENV_PATH
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs.play import play
import os


def init_tts() -> ElevenLabs:
    load_dotenv(ENV_PATH)
    elevenlabs = ElevenLabs(
        api_key=os.getenv("ELEVENLABS_API_KEY"),
    )
    return elevenlabs


def speak(text: str, elevenlabs: ElevenLabs, voice: str, model: str):
    audio = elevenlabs.text_to_speech.convert(
        text=text,
        voice_id=voice,
        model_id=model,
        output_format="mp3_44100_128",
    )

    play(audio)
