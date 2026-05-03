import requests

class AIManager:
    def __init__(self):
        self.mode = "online"

    def toggle(self):
        self.mode = "offline" if self.mode == "online" else "online"
        return self.mode

    def chat(self, prompt, gemini_fn=None):
        # OFFLINE MODE (Ollama)
        if self.mode == "offline":
            try:
                r = requests.post(
                    "http://localhost:11434/api/generate",
                    json={
                        "model": "llama3",
                        "prompt": prompt,
                        "stream": False
                    }
                )
                return r.json().get("response", "")
            except Exception as e:
                return f"[OFFLINE ERROR] {e}"

        # ONLINE MODE (Gemini)
        if gemini_fn:
            return gemini_fn(prompt)

        return "[No AI backend connected]"
