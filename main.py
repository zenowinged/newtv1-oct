from core.speech import speak, listen_command, listen_until_stop
from memory.context_memory import ContextMemory
from core.task_router import handle_command
from core.llm_chat import LocalChatEngine

# Initialize context memory and chat engine
context_memory = ContextMemory()
chat_engine = LocalChatEngine(model_name="phi", memory=context_memory)

def run_assistant():
    speak("Hello Sir, how can I help you today?")

    while True:
        command = listen_command()
        if not command:
            continue

        print(f"Command received: {command}")
        context_memory.add_to_session(f"You: {command}")

        # 🔹 Memory Operations
        if "remember that" in command.lower():
            fact = command.replace("remember that", "", 1).strip()
            context_memory.remember(fact)
            speak("Okay, I've remembered that.")
            continue

        elif "what do you remember" in command.lower():
            facts = context_memory.recall()
            if facts:
                speak("Here's what I remember:")
                for fact in facts[-5:]:
                    speak(fact)
            else:
                speak("I don't remember anything yet.")
            continue

        elif "forget" in command.lower():
            keyword = command.replace("forget", "", 1).strip()
            context_memory.forget(keyword)
            speak(f"I've forgotten anything related to {keyword}.")
            continue

        # 🔹 Chat Mode
        elif "chat with me" in command.lower():
            speak("Entering chat mode. Say 'that's it' to exit.")
            while True:
                user_input = listen_command()
                if not user_input:
                    continue
                if user_input.lower() == "that's it":
                    speak("Exiting chat mode.")
                    break
                context_memory.add_to_session(f"You: {user_input}")
                response = chat_engine.query_llm_with_context(user_input)
                context_memory.add_to_session(f"Assistant: {response}")
                speak(response)
            continue

        # 🔹 Task Routing
        handled = handle_command(command, context_memory)
        if not handled:
            speak("Sorry, I didn't understand that command.")

# 🔹 Run the assistant
if __name__ == "__main__":
    run_assistant()
