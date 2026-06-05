from __future__ import annotations

import json
import os
import sys
import threading
import time
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any

import requests


DEFAULT_REPOSITORY = "turgunovjasur/Playwright"
DEFAULT_WORKFLOW = "daily-smoke.yml"
DEFAULT_REF = "main"
DEFAULT_TARGET = "all"
STATUS_POLL_INTERVAL_SECONDS = 30
STATUS_POLL_ERROR_LIMIT = 5

SERVERS = {
    "smartup": "https://smartup.online",
    "app3": "https://app3.greenwhite.uz/xtrade",
}
SCOPES = {"smoke", "regression"}


class ConfigError(RuntimeError):
    pass


@dataclass(frozen=True)
class RunRequest:
    scope: str
    server_key: str
    server_url: str
    target: str = DEFAULT_TARGET

    @property
    def company_source(self) -> str:
        if self.server_key == "app3":
            return "APP3 secrets"
        return "SMARTUP secrets"


@dataclass(frozen=True)
class WorkflowRun:
    run_id: int | None
    html_url: str


@dataclass(frozen=True)
class ActiveRun:
    chat_id: str
    request: RunRequest
    workflow_run: WorkflowRun
    started_at: float


class ActiveRunStore:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._active: ActiveRun | None = None

    def get(self) -> ActiveRun | None:
        with self._lock:
            return self._active

    def set(self, active: ActiveRun) -> bool:
        with self._lock:
            if self._active is not None:
                return False
            self._active = active
            return True

    def clear(self, run_id: int | None) -> None:
        with self._lock:
            if self._active is None:
                return
            if run_id is None or self._active.workflow_run.run_id == run_id:
                self._active = None


@dataclass(frozen=True)
class BotConfig:
    telegram_token: str
    allowed_chat_ids: set[str]
    github_token: str
    repository: str
    workflow: str
    ref: str
    allowed_server_keys: set[str]


def env_required(name: str, *fallbacks: str) -> str:
    for key in (name, *fallbacks):
        value = os.getenv(key, "").strip()
        if value:
            return value
    names = ", ".join((name, *fallbacks))
    raise ConfigError(f"Required environment variable is missing: {names}")


def env_value(name: str, default: str) -> str:
    return os.getenv(name, default).strip() or default


def split_csv(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def server_keys_from_env(value: str) -> set[str]:
    if not value:
        return set(SERVERS)
    keys: set[str] = set()
    for item in split_csv(value):
        lowered = item.lower().rstrip("/")
        if lowered in SERVERS:
            keys.add(lowered)
            continue
        for key, url in SERVERS.items():
            if lowered == url.rstrip("/"):
                keys.add(key)
                break
    return keys or set(SERVERS)


def load_config() -> BotConfig:
    allowed_chat_ids = set(
        split_csv(os.getenv("TELEGRAM_ALLOWED_CHAT_IDS", "") or os.getenv("TELEGRAM_CHAT_ID", ""))
    )
    if not allowed_chat_ids:
        raise ConfigError("Set TELEGRAM_ALLOWED_CHAT_IDS or TELEGRAM_CHAT_ID to restrict bot access.")

    allowed_server_keys = server_keys_from_env(os.getenv("ALLOWED_SERVER_URLS", ""))

    return BotConfig(
        telegram_token=env_required("TELEGRAM_BOT_TOKEN"),
        allowed_chat_ids=allowed_chat_ids,
        github_token=env_required("GITHUB_TOKEN", "GITHUB_PAT"),
        repository=env_value("GITHUB_REPOSITORY", DEFAULT_REPOSITORY),
        workflow=env_value("GITHUB_WORKFLOW_FILE", DEFAULT_WORKFLOW),
        ref=env_value("GITHUB_REF", DEFAULT_REF),
        allowed_server_keys=allowed_server_keys,
    )


class TelegramClient:
    def __init__(self, token: str) -> None:
        self.base_url = f"https://api.telegram.org/bot{token}"
        self.session = requests.Session()

    def request(self, method: str, payload: dict[str, Any]) -> dict[str, Any]:
        response = self.session.post(f"{self.base_url}/{method}", data=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        if not data.get("ok"):
            raise RuntimeError(f"Telegram API error: {data}")
        return data

    def get_updates(self, offset: int | None) -> list[dict[str, Any]]:
        payload: dict[str, Any] = {"timeout": 50, "allowed_updates": '["message","callback_query"]'}
        if offset is not None:
            payload["offset"] = offset
        return self.request("getUpdates", payload).get("result", [])

    def send_message(self, chat_id: str, text: str, reply_markup: dict[str, Any] | None = None) -> None:
        payload: dict[str, Any] = {
            "chat_id": chat_id,
            "text": text,
            "disable_web_page_preview": "true",
        }
        if reply_markup is not None:
            payload["reply_markup"] = json.dumps(reply_markup)
        self.request("sendMessage", payload)

    def edit_message(self, chat_id: str, message_id: int, text: str) -> None:
        self.request(
            "editMessageText",
            {
                "chat_id": chat_id,
                "message_id": str(message_id),
                "text": text,
                "disable_web_page_preview": "true",
            },
        )

    def answer_callback(self, callback_id: str, text: str = "") -> None:
        payload = {"callback_query_id": callback_id}
        if text:
            payload["text"] = text
        self.request("answerCallbackQuery", payload)


class GitHubActionsClient:
    def __init__(self, token: str, repository: str, workflow: str, ref: str) -> None:
        self.repository = repository
        self.workflow = workflow
        self.ref = ref
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {token}",
                "X-GitHub-Api-Version": "2022-11-28",
            }
        )

    @property
    def workflow_url(self) -> str:
        return f"https://github.com/{self.repository}/actions/workflows/{self.workflow}"

    def dispatch(self, request: RunRequest) -> WorkflowRun:
        started_at = datetime.now(timezone.utc)
        url = f"https://api.github.com/repos/{self.repository}/actions/workflows/{self.workflow}/dispatches"
        response = self.session.post(
            url,
            json={
                "ref": self.ref,
                "inputs": {
                    "scope": request.scope,
                    "server_url": request.server_url,
                    "target": request.target,
                },
            },
            timeout=30,
        )
        if response.status_code != 204:
            raise RuntimeError(f"GitHub dispatch failed: {response.status_code} {response.text}")

        return self.find_new_run(started_at)

    def find_new_run(self, started_at: datetime) -> WorkflowRun:
        deadline = time.monotonic() + 30
        earliest = started_at - timedelta(seconds=15)
        while time.monotonic() < deadline:
            run = self.latest_matching_run(earliest)
            if run is not None:
                return run
            time.sleep(3)
        return WorkflowRun(run_id=None, html_url=self.workflow_url)

    def latest_matching_run(self, earliest: datetime) -> WorkflowRun | None:
        url = f"https://api.github.com/repos/{self.repository}/actions/workflows/{self.workflow}/runs"
        response = self.session.get(
            url,
            params={"branch": self.ref, "event": "workflow_dispatch", "per_page": "10"},
            timeout=30,
        )
        response.raise_for_status()
        runs = response.json().get("workflow_runs", [])
        for item in runs:
            created_at = parse_github_time(str(item.get("created_at", "")))
            if created_at is None or created_at < earliest:
                continue
            run_id = item.get("id")
            html_url = item.get("html_url")
            if isinstance(run_id, int) and isinstance(html_url, str):
                return WorkflowRun(run_id=run_id, html_url=html_url)
        return None

    def get_run_status(self, run_id: int) -> tuple[str, str | None, str]:
        url = f"https://api.github.com/repos/{self.repository}/actions/runs/{run_id}"
        response = self.session.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()
        return str(data.get("status", "")), data.get("conclusion"), str(data.get("html_url", self.workflow_url))


def parse_github_time(value: str) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def help_text() -> str:
    return (
        "Test run qilish uchun /run yuboring.\n\n"
        "Bot avval serverni so'raydi, keyin scope tanlatadi.\n"
        "Company code/password GitHub Secrets'dan olinadi.\n"
        "Test jarayonda bo'lsa yangi /run bloklanadi."
    )


def server_keyboard(config: BotConfig) -> dict[str, Any]:
    rows = []
    if "smartup" in config.allowed_server_keys:
        rows.append([{"text": "smartup.online", "callback_data": "server:smartup"}])
    if "app3" in config.allowed_server_keys:
        rows.append([{"text": "app3.greenwhite.uz/xtrade", "callback_data": "server:app3"}])
    return {"inline_keyboard": rows}


def scope_keyboard(server_key: str) -> dict[str, Any]:
    return {
        "inline_keyboard": [
            [
                {"text": "smoke", "callback_data": f"scope:{server_key}:smoke"},
                {"text": "regression", "callback_data": f"scope:{server_key}:regression"},
            ]
        ]
    }


def active_run_text(active: ActiveRun) -> str:
    elapsed_seconds = max(0, int(time.monotonic() - active.started_at))
    elapsed_minutes = elapsed_seconds // 60
    elapsed_text = "1 daqiqadan kam" if elapsed_minutes == 0 else f"{elapsed_minutes} daqiqa"
    return (
        "Hozir test jarayonda.\n\n"
        f"Server: {active.request.server_url}\n"
        f"Scope: {active.request.scope}\n"
        f"Company: {active.request.company_source}\n"
        f"Vaqt: {elapsed_text}\n"
        f"Run: {active.workflow_run.html_url}\n\n"
        "Test tugagach /run yana ishlaydi."
    )


def show_run_start(
    telegram: TelegramClient,
    chat_id: str,
    config: BotConfig,
    active_store: ActiveRunStore,
) -> None:
    active = active_store.get()
    if active is not None:
        telegram.send_message(chat_id, active_run_text(active))
        return
    telegram.send_message(chat_id, "Qaysi serverda run qilamiz?", reply_markup=server_keyboard(config))


def handle_message(
    telegram: TelegramClient,
    config: BotConfig,
    active_store: ActiveRunStore,
    chat_id: str,
    text: str,
) -> None:
    if chat_id not in config.allowed_chat_ids:
        telegram.send_message(chat_id, "This chat is not allowed to run CI.")
        return

    command = text.split(maxsplit=1)[0].split("@", 1)[0].lower() if text else ""
    if command in {"/start", "/help"}:
        telegram.send_message(chat_id, help_text())
        return
    if command == "/servers":
        lines = [SERVERS[key] for key in sorted(config.allowed_server_keys)]
        telegram.send_message(chat_id, "Ruxsat berilgan serverlar:\n" + "\n".join(lines))
        return
    if command == "/run":
        show_run_start(telegram, chat_id, config, active_store)
        return

    telegram.send_message(chat_id, "Noto'g'ri command. Test run qilish uchun /run yuboring.")


def handle_callback(
    telegram: TelegramClient,
    github: GitHubActionsClient,
    config: BotConfig,
    active_store: ActiveRunStore,
    callback: dict[str, Any],
) -> None:
    callback_id = str(callback.get("id", ""))
    data = str(callback.get("data", ""))
    message = callback.get("message") or {}
    chat = message.get("chat") or {}
    chat_id = str(chat.get("id", ""))
    message_id = message.get("message_id")

    if chat_id not in config.allowed_chat_ids:
        telegram.answer_callback(callback_id, "Not allowed")
        return
    if not isinstance(message_id, int):
        telegram.answer_callback(callback_id)
        return

    active = active_store.get()
    if active is not None:
        telegram.answer_callback(callback_id, "Test jarayonda")
        telegram.send_message(chat_id, active_run_text(active))
        return

    if data.startswith("server:"):
        server_key = data.split(":", 1)[1]
        if server_key not in config.allowed_server_keys or server_key not in SERVERS:
            telegram.answer_callback(callback_id, "Server not allowed")
            return
        telegram.answer_callback(callback_id, "Server tanlandi")
        telegram.edit_message(chat_id, message_id, f"Server tanlandi: {SERVERS[server_key]}")
        telegram.send_message(chat_id, "Qaysi scope bilan run qilamiz?", reply_markup=scope_keyboard(server_key))
        return

    if data.startswith("scope:"):
        parts = data.split(":")
        if len(parts) != 3:
            telegram.answer_callback(callback_id, "Invalid selection")
            return
        _, server_key, scope = parts
        if server_key not in config.allowed_server_keys or server_key not in SERVERS or scope not in SCOPES:
            telegram.answer_callback(callback_id, "Invalid selection")
            return
        telegram.answer_callback(callback_id, "Run boshlanyapti")
        request = RunRequest(scope=scope, server_key=server_key, server_url=SERVERS[server_key])
        start_run(telegram, github, chat_id, message_id, request, active_store)
        return

    telegram.answer_callback(callback_id, "Unknown action")


def start_run(
    telegram: TelegramClient,
    github: GitHubActionsClient,
    chat_id: str,
    message_id: int,
    request: RunRequest,
    active_store: ActiveRunStore,
) -> None:
    telegram.edit_message(
        chat_id,
        message_id,
        (
            "Test boshlanyapti...\n"
            f"Server: {request.server_url}\n"
            f"Scope: {request.scope}\n"
            f"Company: {request.company_source}"
        ),
    )
    try:
        workflow_run = github.dispatch(request)
    except Exception as exc:
        telegram.send_message(chat_id, f"Testni boshlashda xato:\n{exc}")
        return

    if workflow_run.run_id is not None:
        active = ActiveRun(
            chat_id=chat_id,
            request=request,
            workflow_run=workflow_run,
            started_at=time.monotonic(),
        )
        if not active_store.set(active):
            current = active_store.get()
            if current is not None:
                telegram.send_message(chat_id, active_run_text(current))
            return

    telegram.send_message(
        chat_id,
        (
            "GitHub Actions run boshlandi.\n"
            f"Server: {request.server_url}\n"
            f"Scope: {request.scope}\n"
            f"Company: {request.company_source}\n"
            f"Run: {workflow_run.html_url}"
        ),
    )

    if workflow_run.run_id is None:
        telegram.send_message(chat_id, "Run statusini kuzatib bo'lmadi. Natija GitHub Actions linkida ko'rinadi.")
        return

    thread = threading.Thread(
        target=monitor_run,
        args=(telegram, github, chat_id, workflow_run, request, active_store),
        daemon=True,
    )
    thread.start()


def monitor_run(
    telegram: TelegramClient,
    github: GitHubActionsClient,
    chat_id: str,
    workflow_run: WorkflowRun,
    request: RunRequest,
    active_store: ActiveRunStore,
) -> None:
    assert workflow_run.run_id is not None
    started = time.monotonic()
    sent_two_min = False
    sent_five_min = False
    status_errors = 0

    while True:
        elapsed = time.monotonic() - started
        try:
            status, conclusion, html_url = github.get_run_status(workflow_run.run_id)
        except Exception as exc:
            status_errors += 1
            print(
                f"Temporary GitHub status polling error for run {workflow_run.run_id}: {exc}",
                file=sys.stderr,
            )
            if status_errors >= STATUS_POLL_ERROR_LIMIT:
                active_store.clear(workflow_run.run_id)
                telegram.send_message(
                    chat_id,
                    (
                        f"Run statusini {STATUS_POLL_ERROR_LIMIT} marta olishda xato bo'ldi.\n"
                        "Test GitHub Actionsda davom etayotgan bo'lishi mumkin.\n"
                        f"Run: {workflow_run.html_url}"
                    ),
                )
                return
            time.sleep(STATUS_POLL_INTERVAL_SECONDS)
            continue

        status_errors = 0

        if status == "completed":
            active_store.clear(workflow_run.run_id)
            result = (conclusion or "unknown").upper()
            telegram.send_message(
                chat_id,
                (
                    f"Test tugadi: {result}\n"
                    f"Server: {request.server_url}\n"
                    f"Scope: {request.scope}\n"
                    f"Run: {html_url}"
                ),
            )
            return

        if elapsed >= 300 and not sent_five_min:
            telegram.send_message(chat_id, f"Test hali davom etyapti... 5 daqiqa bo'ldi\nRun: {html_url}")
            sent_five_min = True
        elif elapsed >= 120 and not sent_two_min:
            telegram.send_message(chat_id, f"Test davom etyapti... 2 daqiqa bo'ldi\nRun: {html_url}")
            sent_two_min = True

        time.sleep(STATUS_POLL_INTERVAL_SECONDS)


def main() -> int:
    try:
        config = load_config()
    except ConfigError as exc:
        print(exc, file=sys.stderr)
        return 2

    telegram = TelegramClient(config.telegram_token)
    github = GitHubActionsClient(config.github_token, config.repository, config.workflow, config.ref)
    active_store = ActiveRunStore()

    offset: int | None = None
    print(f"Telegram CI bot started for {config.repository}/{config.workflow} on {config.ref}")

    while True:
        try:
            updates = telegram.get_updates(offset)
            for update in updates:
                update_id = update.get("update_id")
                if isinstance(update_id, int):
                    offset = update_id + 1

                message = update.get("message")
                if isinstance(message, dict):
                    chat = message.get("chat") or {}
                    chat_id = str(chat.get("id", ""))
                    text = message.get("text")
                    if isinstance(text, str):
                        handle_message(telegram, config, active_store, chat_id, text.strip())
                    continue

                callback = update.get("callback_query")
                if isinstance(callback, dict):
                    handle_callback(telegram, github, config, active_store, callback)
        except KeyboardInterrupt:
            print("Stopping Telegram CI bot.")
            return 0
        except Exception as exc:
            print(f"Bot loop error: {exc}", file=sys.stderr)
            time.sleep(5)


if __name__ == "__main__":
    raise SystemExit(main())
