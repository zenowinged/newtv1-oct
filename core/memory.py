import os
import json

class Memory:
    def __init__(self, file_path="memory.json"):
        self.file_path = file_path
        self.data = self.load_memory()

    def load_memory(self):
        if os.path.exists(self.file_path) and os.path.getsize(self.file_path) > 0:
            with open(self.file_path, "r") as f:
                try:
                    data = json.load(f)
                    if isinstance(data, list):
                        return data
                    else:
                        return []  # fallback if file was a dict before
                except json.JSONDecodeError:
                    return []
        return []

    def save_memory(self):
        with open(self.file_path, "w") as f:
            json.dump(self.data, f, indent=2)

    def remember_raw(self, statement):
        self.data.append(statement)
        self.save_memory()

    def recall_all(self):
        return self.data

    def forget_all(self):
        self.data = []
        self.save_memory()
