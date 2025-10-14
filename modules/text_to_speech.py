import pyttsx3

tts_engine = pyttsx3.init()
tts_engine.setProperty("rate", 150)
tts_engine.setProperty("volume", 1.0)


def speak(text):
    for segment in text.split(". "):
        if segment.strip():
            tts_engine.say(segment.strip())
            tts_engine.runAndWait()


# import torch
# import soundfile as sf
# from parler_tts import ParlerTTSForConditionalGeneration
# from transformers import AutoTokenizer
# import tempfile
# import os
# import simpleaudio as sa  # pour jouer le son directement en Python

# # Choix du device
# device = (
#     "mps"
#     if torch.backends.mps.is_available()
#     else ("cuda" if torch.cuda.is_available() else "cpu")
# )

# # Chargement du modèle Parler-TTS
# MODEL_NAME = "parler-tts/parler-tts-mini-v1"
# print("[Loading TTS model...]")
# model = ParlerTTSForConditionalGeneration.from_pretrained(MODEL_NAME).to(device)
# tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

# # Description vocale par défaut (modifiable si tu veux une autre voix)
# DESCRIPTION = (
#     "Une femme parle français avec un ton chaleureux, clair et naturel, à un rythme modéré. "
#     "Sa voix est agréable et fluide."
# )


# def speak(text: str):
#     """
#     Génère et joue une sortie vocale à partir du texte donné
#     en utilisant Parler-TTS.
#     """
#     if not text.strip():
#         return

#     try:
#         # Préparation du prompt
#         description_ids = tokenizer(DESCRIPTION, return_tensors="pt").input_ids.to(
#             device
#         )
#         prompt_ids = tokenizer(text, return_tensors="pt").input_ids.to(device)

#         # Génération audio
#         generation = model.generate(
#             input_ids=description_ids,
#             prompt_input_ids=prompt_ids,
#         )

#         # Conversion en numpy
#         audio_arr = generation.cpu().numpy().squeeze()

#         # Sauvegarde temporaire du fichier
#         with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
#             sf.write(tmpfile.name, audio_arr, model.config.sampling_rate)
#             tmp_path = tmpfile.name

#         # Lecture du son
#         wave_obj = sa.WaveObject.from_wave_file(tmp_path)
#         play_obj = wave_obj.play()
#         play_obj.wait_done()

#         # Nettoyage
#         os.remove(tmp_path)

#     except Exception as e:
#         print(f"[TTS Error] {e}")
