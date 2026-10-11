import speech_recognition as sr

def convert_audio_to_text(raw_audio_bytes):
    recognizer = sr.Recognizer()
    audio_obj = sr.AudioData(raw_audio_bytes, 16000, 2)
    try:
        text = recognizer.recognize_google(audio_obj, language="en-IN").strip()
        return text
    except sr.UnknownValueError:
        return None
    except Exception as e:
        print(f"❌ STT Error: {e}")
        return None
