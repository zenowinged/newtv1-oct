from core.speech import speak, listen_command, listen_until_stop
from core.memory import Memory
from core.memory_manager import LLMMemoryManager
from core.llm_chat import LocalChatEngine
import psutil
from modules import (
    open_apps,
    browser_automation,
    system_control,
    system_events,
    general_productivity,
    spotify_control,
)
from modules.system_events import handle_system_event
import datetime


memory = Memory()
llm_memory = LLMMemoryManager()
chat_engine = LocalChatEngine(model_name="phi", memory=memory)

def handle_command(command, memory):
    command = command.lower().strip()

    if "battery" in command or "charge left" in command:
        battery = psutil.sensors_battery()
        if battery:
            percent = battery.percent
            pluggeed = battery.plugged
            status = "plugged in" if pluggeed else "not plugged in"
            speak(f"Battery is at {percent} percent and is {status}.")
        else:
            speak("I couldn't retrieve the battery status.")
        return
    
    elif "what's the time " in command or "what time is it" in command:
        now = datetime.datetime.now()
        speak(f"The current time is {now.strftime('%I:%M %p')}.")
        return
    
    elif "what's the date" in command or "what date is it" in command:
        now = datetime.datetime.now()
        speak(f"The current date is {now.strftime('%B %d, %Y')}.")
        return
    
    
    

    if "chat with me" in command or "let's talk" in command:
        speak("entering chat mode. say'exit chat' anytime to stop.")
        while True:
            user_input = listen_until_stop()
            if "exit chat" in user_input or "stop talking" in user_input:
                speak("Exiting chat mode.")
                break
            reply = chat_engine.chat(user_input)
            speak(reply)
        return
    
    # --------- CORE ACTIONS ---------
    if command.startswith("remember "):
        fact= command.replace("remember ", "", 1).strip()
        memory.remember_raw(fact)
        llm_memory.store(fact)
    
        speak("I will remember that.")
        return

    if "what do you remember" in command or "what's in memory" in command:
        memories = memory.recall_all()
        if memories:
            for mem in memories:
                speak(mem)
        else:
            speak("There's nothing in memory yet.")
        return
    

    elif  "take screenshot" in command or "capture screen" in command:
        import pyautogui
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        path = f"screenshots/screenshot_{timestamp}.png"
        pyautogui.screenshot(path)
        speak(f"Screenshot taken and saved as {path}.")
        return
    


    # --------- POWER & SYSTEM ---------
    if any(word in command for word in ["shutdown", "restart", "lock", "cancel shutdown"]):
        handle_system_event(command)
        return
    

    # --------- APP LAUNCHING ---------
    launch_commands = {
        "start spotify": "spotify",
        "open whatsapp": "whatsapp",
        "open vs code": "vscode",
        "open settings": "settings",
        "open file explorer": "explorer",
        "start vpn": "Proton VPN",
        "open telegram": "telegram",
        "open calculator": "calculator",
        "open command prompt": "cmd",
        "open notepad": "notepad",
        "open spotify": "spotify",
        "launch brave": "brave",
        "open brave": "brave",
        "open chrome": "chrome",
    }
    for key, app in launch_commands.items():
        if key in command:
            open_apps.launch_app(app)
            return

    # --------- SYSTEM CONTROL ---------
    if "set volume to" in command:
        level = int(command.split("set volume to")[-1].strip().replace("%", ""))
        system_control.set_master_volume(level)

    elif "mute system" in command:
        system_control.mute_system(True)
        speak("System muted.")
    elif "unmute system" in command:
        system_control.mute_system(False)
        speak("System unmuted.")
    elif "set brave volume to" in command:
        level = int(command.split("set brave volume to")[-1].strip().replace("%", ""))
        system_control.set_app_volume("brave", level)
    elif "mute brave" in command:
        system_control.mute_app("brave", True)
        speak("Brave muted.")

    elif "unmute brave" in command:
        system_control.mute_app("brave", False)
        speak("Brave unmuted.")
    elif "set spotify volume to" in command:
        level = int(command.split("set spotify volume to")[-1].strip().replace("%", ""))
        system_control.set_app_volume("spotify", level)
    elif "mute spotify" in command:
        system_control.mute_app("spotify", True)
        speak("Spotify muted.")
    elif "unmute spotify" in command:
        system_control.mute_app("spotify", False)
        speak("Spotify unmuted.")

    elif "open downloads" in command:
        import os
        os.startfile(os.path.join(os.path.expanduser("~"), "Downloads"))

    elif "open documents" in command:
        import os
        os.startfile(os.path.join(os.path.expanduser("~"), "Documents"))
    elif "open desktop" in command:
        import os
        os.startfile(os.path.join(os.path.expanduser("~"), "Desktop"))
    elif "open control panel" in command:
        import subprocess
        subprocess.Popen(["control", "panel"])
        return
    elif "open task manager" in command:
        import subprocess
        subprocess.Popen(["taskmgr"])
        return
    elif "open run" in command:
        import subprocess
        subprocess.Popen(["win+r"])
        return
    elif "open terminal" in command or "open command line" in command:
        import subprocess
        subprocess.Popen(["cmd"])
        return
    elif "open powershell" in command:
        import subprocess
        subprocess.Popen(["powershell"])
        return
    elif "open system info" in command:
        import subprocess
        subprocess.Popen(["msinfo32"])
        return
    elif "open registry editor" in command:
        import subprocess
        subprocess.Popen(["regedit"])
        return
    elif "open task scheduler" in command:
        import subprocess
        subprocess.Popen(["taskschd.msc"])
        return
    elif "open magnifier" in command:
        import subprocess
        subprocess.Popen(["magnify"])
        return
    elif "open snipping tool" in command:
        import subprocess
        subprocess.Popen(["snippingtool"])
        return
    elif "open sticky notes" in command:
        import subprocess
        subprocess.Popen(["stikynot"])
        return
    elif "open calculator" in command:
        import subprocess
        subprocess.Popen(["calc"])
        return
    elif "open notepad" in command:
        import subprocess
        subprocess.Popen(["notepad"])
        return
    elif "open paint" in command:
        import subprocess
        subprocess.Popen(["mspaint"])
        return
    elif "open file explorer" in command or "open my computer" in command:
        import subprocess
        subprocess.Popen(["explorer"])
        return
    elif "open control panel" in command:
        import subprocess
        subprocess.Popen(["control"])
        return
    elif "open settings" in command:
        import subprocess
        subprocess.Popen(["start", "ms-settings:"])
        return
    

    
    # --------- YOUTUBE & MEDIA ---------
    if "youtube" in command and "play" in command:
        browser_automation.play_youtube_video(command)
        return

    # --------- SPOTIFY CONTROL ---------
    if "pause spotify" in command:
        spotify_control.pause()
        return
    if "play spotify" in command:
        spotify_control.play()
        return
    if "next song" in command:
        spotify_control.next_track()
        return
    if "previous song" in command:
        spotify_control.previous_track()
        return
    if "play song" in command:
        song_name = command.replace("play song", "").strip()
        if song_name:
            spotify_control.play_song(song_name)
        else:
            speak("Please specify a song name to play.")            
    
        return
    # --------- PRODUCTIVITY ---------
    if "add to do" in command:
        general_productivity.create_todo("Send email to team")
        return
    if "start a google meet" in command or "start meet" in command:
        general_productivity.launch_google_meet()
        return
    if "start timer" in command:
        general_productivity.set_timer_from_command(command)
        return
    



    # --------- WEBSITE OPENERS ---------
    web_links = {
        "open instagram": "https://instagram.com",
        "login to instagram": "https://instagram.com",
        "open facebook": "https://facebook.com",
        "login to facebook": "https://facebook.com",
        "open twitter": "https://twitter.com",
        "login to twitter": "https://twitter.com",
        "open linkedin": "https://linkedin.com",
        "login to linkedin": "https://linkedin.com",
        "open github": "https://github.com",
        "login to github": "https://github.com",
        "open chat gpt": "https://chat.openai.com",
        "login to chatgpt": "https://chat.openai.com",
        "open google": "https://google.com",
        "login to google": "https://google.com",
        "open mail": "https://mail.google.com",
        "login to mail": "https://mail.google.com",
        "open drive": "https://drive.google.com",
        "login to drive": "https://drive.google.com",
        "open youtube studio": "https://studio.youtube.com",
        "login to youtube studio": "https://studio.youtube.com",
        "open hotstar": "https://www.hotstar.com",
        "login to hotstar": "https://www.hotstar.com",
        "open tracker": "https://www.google.com/android/find/u/5/?login&pli=1",
        "open google photos": "https://photos.google.com",
        "open calender": "https://calendar.google.com",
        "open google maps": "https://maps.google.com",
        "open google docs": "https://docs.google.com",
        "open google sheets": "https://sheets.google.com",
        "open google slides": "https://slides.google.com",
        "open google keep": "https://keep.google.com",
        "open spotify web": "https://open.spotify.com",
        "open netflix": "https://www.netflix.com",
        "open hotstar": "https://www.hotstar.com",
        "open prime video": "https://www.primevideo.com",
        "open amazon": "https://www.amazon.in",
        "open flipkart": "https://www.flipkart.com",
        "open quora": "https://www.quora.com",
        "open stack overflow": "https://stackoverflow.com",
        "open reddit": "https://www.reddit.com",
        "open wikipedia": "https://www.wikipedia.org",
        "open medium": "https://www.medium.com",
        "open whats app web": "https://web.whatsapp.com",
        "open telegram web": "https://web.telegram.org",
        "open discord": "https://discord.com",
        "open slack": "https://slack.com",
        "open twitter": "https://x.com",
        

       


    }

    for trigger, url in web_links.items():
        if trigger in command:
            browser_automation.open_website(url)
            return

    # --------- FINAL CATCH ---------
    speak("Sorry, I didn't understand that command.")
