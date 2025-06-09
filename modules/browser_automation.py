# modules/browser_automation.py

import webbrowser

def play_video(query):
    print(f"🎬 Playing video: {query}")
    url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
    webbrowser.open(url)

def play_youtube_video(command):
    # crude way to extract what to play
    if "play" in command:
        search_term = command.split("play", 1)[1].strip()
    else:
        search_term = "lofi"

    print(f"🎬 Playing video: {search_term}")
    webbrowser.open(f"https://www.youtube.com/results?search_query={search_term}")


def open_website(site):
    print(f"🌐 Opening: {site}")
    webbrowser.open(site)


def login_website(name):
    print(f"🔐 Attempting login to {name} (placeholder)")
