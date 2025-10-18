from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs.play import play
import os

load_dotenv()

elevenlabs = ElevenLabs(
    api_key=os.getenv("ELEVENLABS_API_KEY"),
)

####
# Voice
Viking_id = "ljo9gAlSqKOvF6D8sOsX"
Rulia_id = "McVZB9hVxVSk3Equu8EH"

# Model
v3_model = "eleven_v3"
v2_model = "eleven_multilingual_v2"
flash_v2_5_model = "eleven_flash_v2_5"
####

audio = elevenlabs.text_to_speech.convert(
    text="Odin est un jeu de société stratégique inspiré de la mythologie nordique, où chaque joueur incarne un clan viking cherchant à gagner gloire et pouvoir.",
    voice_id=Rulia_id,
    model_id=flash_v2_5_model,
    output_format="mp3_44100_128",
)

play(audio)
