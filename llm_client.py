"""Local Llama 3.1 8B client (Ollama). Replaces anthropic.Anthropic()."""
import requests

HOST = "http://localhost:11434"
MODEL = "llama3.1:8b"


def chat(messages: list, system: str = "", tools: list = None, json_mode: bool = False) -> dict:
    """Send a chat request to Ollama and return the assistant message dict."""
    payload = {
        "model": MODEL,
        "messages": ([{"role": "system", "content": system}] if system else []) + messages,
        "stream": False,
        "options": {"temperature": 0.2},
    }
    if tools:
        payload["tools"] = tools
    if json_mode:
        payload["format"] = "json"
    r = requests.post(f"{HOST}/api/chat", json=payload, timeout=300)
    r.raise_for_status()
    return r.json()["message"]
