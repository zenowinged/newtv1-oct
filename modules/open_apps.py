# modules/open_apps.py

import subprocess
import json
import os

APP_PATHS_FILE = "data/app_paths.json"


class Memory:
    def __init__(self, file_path="memory.json"):
        self.file_path = file_path
        self.data = self.load_memory()

    def load_memory(self):
        if os.path.exists(self.file_path) and os.path.getsize(self.file_path) > 0:
            with open(self.file_path, "r") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return {}
        return {}

    def save_memory(self):
        with open(self.file_path, "w") as f:
            json.dump(self.data, f, indent=4)

    def remember(self, key, value):
        self.data[key] = value
        self.save_memory()

    def recall(self, key):
        return self.data.get(key, None)

    def forget(self, key):
        if key in self.data:
            del self.data[key]
            self.save_memory()

def load_app_paths():
    if os.path.exists(APP_PATHS_FILE):
        with open(APP_PATHS_FILE, 'r') as f:
            return json.load(f)
    return {}

def launch_app(app_name):
    apps = load_app_paths()
    path = apps.get(app_name.lower())
    if path:
        print(f"🚀 Launching {app_name}")
        subprocess.Popen(path)
    else:
        print(f"❌ App '{app_name}' not found in app_paths.json")
