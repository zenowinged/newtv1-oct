import speech_recognition as sr

recogniser = sr.Recognizer()
mic = sr.Microphone()

def listen_command():
    with mic as source:
        recogniser.adjust_for_ambient_noise(source, duration=1)
        print("🗣️ Listening for command...")
        try:
            audio = recogniser.listen(source, timeout=5, phrase_time_limit=7)
            command = recogniser.recognize_google(audio)
            print(f"🎤 You said: {command}")
            return command.lower()
        except sr.WaitTimeoutError:
            print("⏱️ Listening timed out. No speech detected.")
            return ""
        except sr.UnknownValueError:
            print("❓ Sorry, I couldn't understand that.")
            return ""
        except sr.RequestError:
            print("🚫 Could not request results from speech recognition service.")
            return ""
