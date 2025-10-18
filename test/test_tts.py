import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from modules.text_to_speech import speak, init_tts
from config import VIKING_ID, FLASH_2_5_MODEL


text = "Odin est un jeu de société stratégique inspiré de la mythologie nordique..."

tts_pipe = init_tts()

speak(text, tts_pipe, VIKING_ID, FLASH_2_5_MODEL)
