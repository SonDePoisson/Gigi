from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs.play import play
import os

load_dotenv()

elevenlabs = ElevenLabs(
    api_key=os.getenv("ELEVENLABS_API_KEY"),
)

audio = elevenlabs.text_to_speech.convert(
    text="Odin est un jeu de société stratégique inspiré de la mythologie nordique, où chaque joueur incarne un clan viking cherchant à gagner gloire et pouvoir. Le but est de gérer ses ressources, explorer de nouvelles terres, recruter des guerriers et accomplir des quêtes tout en affrontant d’autres joueurs ou des événements aléatoires. Le jeu combine placement de tuiles ou de pions, gestion de ressources et planification tactique, avec une part de hasard liée aux combats et aux événements, ce qui exige de s’adapter constamment pour maximiser ses points de victoire et devenir le clan le plus influent.",
    voice_id="JBFqnCBsd6RMkjVDRZzb",
    model_id="eleven_v3",
    output_format="mp3_44100_128",
)

# audio = elevenlabs.text_to_sound_effects.convert(text="Cinematic Braam, Horror")

play(audio)
