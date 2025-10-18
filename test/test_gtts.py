from gtts import gTTS
import subprocess

text = "Odin est un jeu de société stratégique inspiré de la mythologie nordique..."

output_file = "output.mp3"
tts = gTTS(text=text, lang="fr")
tts.save(output_file)

# Lecture audio avec afplay (macOS)
subprocess.run(["afplay", output_file])
