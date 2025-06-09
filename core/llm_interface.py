import requests
from core.speech import speak


def query_llm(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "phi", "prompt": prompt, "stream": False}
        )
        if response.ok:
            result = response.json().get("response", "").strip()
        else:
            result = "❌ Error from LLM: " + response.text
    except Exception as e:
        result = f"❌ Failed to contact LLM: {e}"

    # Check if the command is "chatty" (not a system/task command)
    if not any(keyword in prompt for keyword in ["open", "start", "shutdown", "remember", "launch", "play", "create", "delete", "mute", "unmute", "set", "toggle"]):
        result = query_llm(prompt)
        speak(result)

    return result