"""
Telegram bot — tugma orqali regression testlarni ishga tushirish.
Faqat TELEGRAM_CHAT_ID egasi (admin) boshqara oladi.

Ishga tushirish: start_bot.bat
Buyruqlar:
  /start — boshqaruv paneli
  /run   — boshqaruv paneli
  /id    — foydalanuvchi ID sini ko'rsatadi
"""
import json
import logging
import os
import subprocess
import time
from pathlib import Path

import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# ── .env yuklash ──────────────────────────────────────────────────────────────

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
            key, val = key.strip(), val.strip()
            if key and key not in os.environ:
                os.environ[key] = val

_load_env()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
ADMIN_ID  = int(os.getenv("TELEGRAM_CHAT_ID", "0"))
BAT_FILE  = Path(__file__).parent.parent / "run_tests.bat"
BASE_URL  = f"https://api.telegram.org/bot{BOT_TOKEN}"

_current_proc: subprocess.Popen | None = None


# ── Telegram API ───────────────────────────────────────────────────────────────

def _api(method: str, **kwargs) -> dict:
    try:
        r = requests.post(f"{BASE_URL}/{method}", json=kwargs, timeout=30)
        return r.json()
    except Exception as e:
        logging.error("API xatosi %s: %s", method, e)
        return {}


def _send(chat_id: int, text: str, reply_markup: dict | None = None) -> int | None:
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
    if reply_markup:
        payload["reply_markup"] = reply_markup
    data = _api("sendMessage", **payload)
    result = data.get("result", {})
    return result.get("message_id")


def _edit(chat_id: int, message_id: int, text: str, reply_markup: dict | None = None) -> None:
    payload = {"chat_id": chat_id, "message_id": message_id, "text": text, "parse_mode": "HTML"}
    if reply_markup:
        payload["reply_markup"] = reply_markup
    _api("editMessageText", **payload)


def _answer(callback_id: str, text: str = "") -> None:
    _api("answerCallbackQuery", callback_query_id=callback_id, text=text)


# ── Yordamchi ─────────────────────────────────────────────────────────────────

def _is_running() -> bool:
    return _current_proc is not None and _current_proc.poll() is None


def _run_keyboard() -> dict:
    label = "⏳ Ishlamoqda..." if _is_running() else "🚀 Run Tests Now"
    return {"inline_keyboard": [[{"text": label, "callback_data": "run_tests"}]]}


# ── Xabar va callback handlerlari ─────────────────────────────────────────────

def _handle_message(msg: dict) -> None:
    chat_id = msg.get("chat", {}).get("id", 0)
    text    = (msg.get("text") or "").strip()
    uid     = msg.get("from", {}).get("id", 0)

    command = text.split(maxsplit=1)[0].split("@", 1)[0].lower() if text else ""

    if command == "/id":
        match = "✅ HA" if uid == ADMIN_ID else "❌ YO'Q"
        _send(chat_id,
              f"Sizning Telegram ID: <code>{uid}</code>\n"
              f"Bot admin ID: <code>{ADMIN_ID}</code>\n"
              f"Mos keladi: {match}")
        return

    if uid != ADMIN_ID:
        return

    if command in ("/start", "/run"):
        _send(chat_id, "Regression test boshqaruv paneli:", reply_markup=_run_keyboard())


def _handle_callback(cb: dict) -> None:
    global _current_proc
    cid     = str(cb.get("id", ""))
    uid     = cb.get("from", {}).get("id", 0)
    data    = cb.get("data", "")
    message = cb.get("message", {})
    chat_id = message.get("chat", {}).get("id", 0)
    msg_id  = message.get("message_id", 0)

    _answer(cid)

    if uid != ADMIN_ID:
        return

    if data != "run_tests":
        return

    if _is_running():
        _edit(chat_id, msg_id,
              "⚠️ Testlar hozir allaqachon ishlamoqda.\n"
              "Tugashini kuting — natijalar shu chatga keladi.",
              reply_markup=_run_keyboard())
        return

    try:
        _current_proc = subprocess.Popen(
            ["cmd", "/c", str(BAT_FILE)],
            cwd=str(BAT_FILE.parent),
            creationflags=0x08000000,  # CREATE_NO_WINDOW
        )
        logging.info("Test ishga tushirildi, PID=%s", _current_proc.pid)
        _edit(chat_id, msg_id,
              "⏳ Regression testlar ishga tushirildi...\n"
              "Barcha formalar tekshiriladi (~5-8 daqiqa).\n"
              "Natijalar shu chatga keladi.",
              reply_markup=_run_keyboard())
    except Exception as e:
        logging.exception("Subprocess ishga tushirilmadi")
        _edit(chat_id, msg_id,
              f"❌ Testlarni ishga tushirib bo'lmadi:\n<code>{e}</code>",
              reply_markup=_run_keyboard())


# ── Main loop ─────────────────────────────────────────────────────────────────

def main() -> None:
    if not BOT_TOKEN:
        raise RuntimeError(".env da TELEGRAM_BOT_TOKEN topilmadi")
    if not ADMIN_ID:
        raise RuntimeError(".env da TELEGRAM_CHAT_ID topilmadi")
    if not BAT_FILE.exists():
        raise RuntimeError(f"run_tests.bat topilmadi: {BAT_FILE}")

    logging.info("Bot ishga tushdi. Admin ID: %s | BAT: %s", ADMIN_ID, BAT_FILE)

    offset: int | None = None
    while True:
        try:
            payload: dict = {"timeout": 50, "allowed_updates": ["message", "callback_query"]}
            if offset is not None:
                payload["offset"] = offset
            data = _api("getUpdates", **payload)
            updates = data.get("result", [])

            for upd in updates:
                update_id = upd.get("update_id")
                if isinstance(update_id, int):
                    offset = update_id + 1

                if "message" in upd:
                    _handle_message(upd["message"])
                elif "callback_query" in upd:
                    _handle_callback(upd["callback_query"])

        except KeyboardInterrupt:
            logging.info("Bot to'xtatildi.")
            break
        except Exception as e:
            logging.error("Loop xatosi: %s", e)
            time.sleep(5)


if __name__ == "__main__":
    main()
