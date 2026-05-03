import requests

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL = "llama3"

OFFLINE_MODE = False


def set_mode(state: bool):
    global OFFLINE_MODE
    OFFLINE_MODE = state


def is_offline():
    return OFFLINE_MODE


def ask(prompt: str, online_fn=None):
    if OFFLINE_MODE:
        try:
            response = requests.post(
                OLLAMA_URL,
                json={
                    "model": MODEL,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=60
            )

            data = response.json()
            return data.get("response", "")

        except Exception as e:
            return f"[OFFLINE ERROR] {e}"

    if online_fn:
        return online_fn(prompt)

    return "No online backend connected."
