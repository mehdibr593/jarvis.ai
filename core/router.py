
import requests

AI_MODE = "online"

def set_mode(mode):
    global AI_MODE
    AI_MODE = mode

def get_mode():
    return AI_MODE

def route_ai(prompt, gemini_fn=None):
    if AI_MODE == "offline":
        try:
            r = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": "llama3", "prompt": prompt, "stream": False}
            )
            return r.json().get("response", "")
        except Exception as e:
            return f"[OFFLINE ERROR] {e}"

    if gemini_fn:
        return gemini_fn(prompt)

    return "No AI backend connected"
