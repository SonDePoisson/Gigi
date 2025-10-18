from gtts import gTTS
import tempfile
import playsound


def speak(text: str, lang: str = "fr"):
    """Convertit le texte en audio et le joue en français par défaut."""
    tts = gTTS(text=text, lang=lang)

    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
        tts.save(f.name)
        path = f.name

    playsound.playsound(path, block=True)
