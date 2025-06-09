import os
import subprocess
import ctypes
from core.speech import speak
from core.voice_interface import listen_command  # optional for voice confirmation

# --- Toggle this to True if you want to use voice to confirm ---
USE_VOICE_CONFIRMATION = False

def ask_for_confirmation(prompt):
    """Ask user for confirmation (voice or text)."""
    speak(prompt + " Say yes or no.")
    
    if USE_VOICE_CONFIRMATION:
        response = listen_command().lower()
    else:
        response = input(f"{prompt} (yes/no): ").strip().lower()
        
    return "yes" in response

def shutdown_system():
    if ask_for_confirmation("Are you sure you want to shut down?"):
        speak("Shutting down.")
        subprocess.call(["shutdown", "/s", "/t", "0"])
    else:
        speak("Shutdown cancelled.")

def restart_system():
    if ask_for_confirmation("Are you sure you want to restart?"):
        speak("Restarting.")
        subprocess.call(["shutdown", "/r", "/t", "0"])
    else:
        speak("Restart cancelled.")

def lock_system():
    speak("Locking your system.")
    ctypes.windll.user32.LockWorkStation()

def cancel_shutdown():
    os.system("shutdown /a")
    speak("Scheduled shutdown cancelled.")

def handle_system_event(command: str):
    command = command.lower().strip()

    if "shutdown" in command and "restart" not in command:
        shutdown_system()
    elif "restart" in command:
        restart_system()
    elif "lock" in command:
        lock_system()
    elif "cancel shutdown" in command:
        cancel_shutdown()
    else:
        speak("Unknown system command.")
