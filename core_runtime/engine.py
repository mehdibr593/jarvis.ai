import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def ask(prompt: str, model="llama3"):
    try:
        r = requests.post(
            OLLAMA_URL,
            json={"model": model, "prompt": prompt, "stream": False},
            timeout=60
        )
        return r.json().get("response", "")
    except Exception:
        return "Offline mode unavailable (start Ollama)"
