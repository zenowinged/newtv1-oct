import subprocess

class LocalChatEngine:
    def __init__(self, model_name="mistral", memory=None):
        self.model = model_name
        self.history = []
        self.memory = memory

        if memory:
            # recall_all() should return a list of remembered facts
            remembered_facts = memory.recall_all()
            if remembered_facts:
                context_block = "\n".join([f"User told me: {fact}" for fact in remembered_facts])
                self.history.append({"role": "system", "content": context_block})

    def query_llm_with_context(self, user_input):
        if self.memory:
            context = self.memory.build_context(user_input)
            self.history.append({"role": "user", "content": f"{user_input}\n\nContext: {context}"})
        else:
            self.history.append({"role": "user", "content": user_input})

        prompt = self.format_prompt()
        response = self.query_ollama(prompt)
        self.history.append({"role": "assistant", "content": response})
        return response

    def query_ollama(self, prompt):
        command = ["ollama", "run", self.model]
        try:
            process = subprocess.Popen(
                command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout, stderr = process.communicate(prompt)
            if stderr:
                # Optional: handle or log stderr if needed
                pass
            return stdout.strip()
        except Exception as e:
            return f"Error communicating with the local model: {e}"

    def format_prompt(self):
        # Limit prompt to last 12 messages for context window
        return "\n".join([f"{msg['role']}: {msg['content']}" for msg in self.history[-12:]])
