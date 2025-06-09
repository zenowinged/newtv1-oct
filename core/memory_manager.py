import json
import os
from datetime import datetime

MEMORY_FILE = "data/memories.jsonl"

class LLMMemoryManager:
    def __init__(self):
        os.makedirs("data", exist_ok=True)
        if not os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, "w") as f:
                pass

    def store(self, text):
        memory = {
            "input": text,
            "timestamp": datetime.now().isoformat()
        }
        with open(MEMORY_FILE, "a") as f:
            f.write(json.dumps(memory) + "\n")

    def recall(self, keyword):
        results = []
        with open(MEMORY_FILE, "r") as f:
            for line in f:
                entry = json.loads(line)
                if keyword.lower() in entry["input"].lower():
                    results.append(entry)
        return results
