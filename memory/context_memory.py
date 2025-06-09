import json
import os 
from datetime import datetime


class ContextMemory:
    def __init__(self, memory_file="memory/persistent.json"):
        self.session_memory = []
        self.memory_file = memory_file
        self.load_memory()

    def load_memory(self):
        try:
            if os.path.exists(self.memory_file):
                with open(self.memory_file, "r") as f:
                    self.persistent_memory = json.load(f)
            else:
                self.persistent_memory = {}
        except Exception as e:
            print(f"[ERROR] Failed to load memory: {e}")
            self.persistent_memory = {}

    def save_memory(self):
        with open(self.memory_file, "w") as file:
            json.dump(self.session_memory, file, indent=4)
    
    def remember(self, fact):
        timestamp = datetime.now().isoformat()
        self.persist_memory[timestamp] = fact
        self.save_memory()

    def forget(self, keyword):
        keys_to_delete = [k for k, v in self.persist_memory.items() if keyword.lower() in v.lower()]
        for k in keys_to_delete:
            del self.persist_memory[k]
        self.save_memory()

    def recall(self, keyword=None):
        if keyword:
            return [v for v in self.persistent_memory.values() if keyword.lower() in v.lower()]
        return list(self.persistent_memory.values())

    def recall_all(self):  # Just an alias for compatibility
        return self.recall()

    
    def add_to_session(self, text):
        self.session_memory.append(text)
        if len(self.session_memory) > 10:
            self.session_memory.pop(0)

    def get_session_context(self):
        return "\n".join(self.session_memory)

    def build_context(self, current_input):
        persistent = "\n".join(self.recall())
        session = self.get_session_context()
        return f"Persistent Memory:\n{persistent}\n\nRecent Conversation:\n{session}\n\nUser: {current_input}"
   