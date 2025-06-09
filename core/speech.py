import pyttsx3
import speech_recognition as sr

engine = pyttsx3.init()
engine.setProperty('rate', 180)

def speak(text):
    print(f"🔊 Speaking: {text}")
    engine.say(text)
    engine.runAndWait()

def listen_command(timeout=5, phrase_time_limit=10):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🗣️ Listening for command...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            command = recognizer.recognize_google(audio)
            print(f"🎤 You said: {command}")
            return command.lower()
        except sr.WaitTimeoutError:
            print("⏱️ Listening timed out. No speech detected.")
        except sr.UnknownValueError:
            print("🤷 Couldn't understand audio.")
        except sr.RequestError as e:
            print(f"⚠️ Error with speech recognition: {e}")
    return ""

def listen_until_stop(stop_phrase="that's it"):
    recognizer = sr.Recognizer()
    full_text = []
    print(f"Listening continuously... (say '{stop_phrase}' to stop)")

    while True:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                command = recognizer.recognize_google(audio).lower()
                print(f"🎤 You said: {command}")
                if stop_phrase in command:
                    break
                full_text.append(command)
            except sr.WaitTimeoutError:
                print("⏱️ Listening timeout.")
            except sr.UnknownValueError:
                print("🤷 Couldn't understand audio.")
            except sr.RequestError as e:
                print(f"⚠️ Speech recognition error: {e}")
    return " ".join(full_text)
