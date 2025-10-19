from modules.speech_to_text import transcribe, init_asr
from modules.text_to_speech import speak, init_tts
from modules.brain import generate_response
from config import BAD_PATTERNS, SAMPLE_RATE, FLASH_2_5_MODEL, VIKING_ID

import speech_recognition as sr
import time


def main():
    recognizer = sr.Recognizer()
    mic = sr.Microphone(sample_rate=SAMPLE_RATE)
    asr_pipeline = init_asr()
    elevenlab_pipe = init_tts("Eleven")  # Add 'Eleven' to use ElevenLabs

    print("Listening... (press Ctrl+C to stop)")

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)

        while True:
            try:
                recognizer.pause_threshold = 2.0
                print("[Listening]")
                audio = recognizer.listen(source)
                print("[Processing]")

                text = transcribe(asr_pipeline, audio)

                if text and all(bad not in text for bad in BAD_PATTERNS):
                    print(f"User: {text}")
                    print("[Thinking]")
                    answer = generate_response(text)
                    print(f"AI: {answer}")
                    print("[Speaking]")
                    speak(answer, elevenlab_pipe, VIKING_ID, FLASH_2_5_MODEL)
                    # speak(answer)

            except KeyboardInterrupt:
                print("\nListening stopped.")
                break
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(1)


if __name__ == "__main__":
    main()
