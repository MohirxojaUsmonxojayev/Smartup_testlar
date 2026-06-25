import os
import requests
from pathlib import Path

_MAX_LEN = 4000


def _load_env() -> None:
    env_file = Path(__file__).parent.parent / ".env"
    if not env_file.exists():
        return
    with open(env_file, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, val = line.partition("=")
            key = key.strip()
            val = val.strip()
            if key and key not in os.environ:
                os.environ[key] = val


_load_env()


def send_telegram(text: str) -> bool:
    token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id = os.getenv("TELEGRAM_CHAT_ID", "").strip()
    if not token or not chat_id:
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    ok = True
    for part in _split(text):
        try:
            r = requests.post(
                url,
                json={"chat_id": chat_id, "text": part, "parse_mode": "HTML"},
                timeout=15,
            )
            if not r.ok:
                ok = False
        except Exception:
            ok = False
    return ok


def _split(text: str) -> list:
    if len(text) <= _MAX_LEN:
        return [text]
    parts = []
    while text:
        if len(text) <= _MAX_LEN:
            parts.append(text)
            break
        idx = text.rfind("\n", 0, _MAX_LEN)
        if idx <= 0:
            idx = _MAX_LEN
        parts.append(text[:idx])
        text = text[idx:].lstrip("\n")
    return parts
