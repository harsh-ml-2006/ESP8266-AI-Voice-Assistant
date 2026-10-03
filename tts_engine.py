import pyttsx3

def initialize_voice():
    engine = pyttsx3.init()
    engine.setProperty('rate', 160)
    engine.setProperty('volume', 1.0)
    
    # Set to female/Indian voice if available
    voices = engine.getProperty('voices')
    for voice in voices:
        if 'Zira' in voice.name or 'India' in voice.name:
            engine.setProperty('voice', voice.id)
            break
    return engine

def speak_text(text):
    engine = initialize_voice()
    print("AI Speaking:", text)
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    speak_text("Hello CN Sir, our team is ready with the project.")
