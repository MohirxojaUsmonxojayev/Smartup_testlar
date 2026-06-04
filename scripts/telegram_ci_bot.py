from __future__ import annotations

import os
import shlex
import sys
import time
from dataclasses import dataclass
from typing import Any

import requests


DEFAULT_REPOSITORY = "turgunovjasur/Playwright"
DEFAULT_WORKFLOW = "daily-smoke.yml"
DEFAULT_REF = "main"
DEFAULT_SCOPE = "smoke"
DEFAULT_TARGET = "all"
DEFAULT_SERVER_URL = "https://smartup.online/"
VALID_SCOPES = {"smoke", "regression"}
VALID_TARGETS = {"all", "setup", "group-a", "group-b"}


class ConfigError(RuntimeError):
    pass


def env_required(name: str, *fallbacks: str) -> str:
    for key in (name, *fallbacks):
        value = os.getenv(key, "").strip()
        if value:
            return value
    names = ", ".join((name, *fallbacks))
    raise ConfigError(f"Required environment variable is missing: {names}")


def env_value(name: str, default: str) -> str:
    return os.getenv(name, default).strip() or default


def normalize_url(value: str) -> str:
    return value.strip().rstrip("/")


def split_csv(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


@dataclass(frozen=True)
class RunRequest:
    scope: str
    server_url: str
    target: str


@dataclass(frozen=True)
class BotConfig:
    telegram_token: str
    allowed_chat_ids: set[str]
    github_token: str
    repository: str
    workflow: str
    ref: str
    default_server_url: str
    allowed_server_urls: set[str]
    allow_any_server: bool


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
        payload: dict[str, Any] = {"timeout": 50, "allowed_updates": '["message"]'}
        if offset is not None:
            payload["offset"] = offset
        return self.request("getUpdates", payload).get("result", [])

    def send_message(self, chat_id: str, text: str) -> None:
        self.request(
            "sendMessage",
            {
                "chat_id": chat_id,
                "text": text,
                "disable_web_page_preview": "true",
            },
        )


class GitHubActionsClient:
    def __init__(self, token: str, repository: str, workflow: str, ref: str) -> None:
        self.token = token
        self.repository = repository
        self.workflow = workflow
        self.ref = ref
        self.session = requests.Session()

    @property
    def workflow_url(self) -> str:
        return f"https://github.com/{self.repository}/actions/workflows/{self.workflow}"

    def dispatch(self, request: RunRequest) -> str:
        url = f"https://api.github.com/repos/{self.repository}/actions/workflows/{self.workflow}/dispatches"
        response = self.session.post(
            url,
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {self.token}",
                "X-GitHub-Api-Version": "2022-11-28",
            },
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
        if response.status_code not in {200, 204}:
            raise RuntimeError(f"GitHub dispatch failed: {response.status_code} {response.text}")
        if response.status_code == 200:
            data = response.json()
            html_url = data.get("html_url")
            if html_url:
                return str(html_url)
        return self.workflow_url


def load_config() -> BotConfig:
    default_server_url = normalize_url(env_value("DEFAULT_SERVER_URL", DEFAULT_SERVER_URL))
    allowed_servers_raw = env_value("ALLOWED_SERVER_URLS", default_server_url)
    allow_any_server = allowed_servers_raw.strip() == "*"
    allowed_server_urls = {normalize_url(item) for item in split_csv(allowed_servers_raw)}

    allowed_chat_ids = set(
        split_csv(os.getenv("TELEGRAM_ALLOWED_CHAT_IDS", "") or os.getenv("TELEGRAM_CHAT_ID", ""))
    )
    if not allowed_chat_ids:
        raise ConfigError("Set TELEGRAM_ALLOWED_CHAT_IDS or TELEGRAM_CHAT_ID to restrict bot access.")

    return BotConfig(
        telegram_token=env_required("TELEGRAM_BOT_TOKEN"),
        allowed_chat_ids=allowed_chat_ids,
        github_token=env_required("GITHUB_TOKEN", "GITHUB_PAT"),
        repository=env_value("GITHUB_REPOSITORY", DEFAULT_REPOSITORY),
        workflow=env_value("GITHUB_WORKFLOW_FILE", DEFAULT_WORKFLOW),
        ref=env_value("GITHUB_REF", DEFAULT_REF),
        default_server_url=default_server_url,
        allowed_server_urls=allowed_server_urls,
        allow_any_server=allow_any_server,
    )


def help_text(config: BotConfig) -> str:
    allowed_servers = "any" if config.allow_any_server else ", ".join(sorted(config.allowed_server_urls))
    return (
        "Smartup CI bot commands:\n"
        "/smoke - run smoke tests on default server\n"
        "/regression - run regression tests on default server\n"
        "/run scope=smoke server=https://smartup.online target=all\n"
        "/run smoke https://smartup.online\n"
        "/servers - show allowed servers\n\n"
        f"Default server: {config.default_server_url}\n"
        f"Allowed servers: {allowed_servers}\n"
        "Targets: all, setup, group-a, group-b"
    )


def parse_run_request(text: str, config: BotConfig) -> RunRequest:
    parts = text.strip().split(maxsplit=1)
    command = parts[0].split("@", 1)[0].lower()
    args_text = parts[1] if len(parts) > 1 else ""

    scope = DEFAULT_SCOPE
    target = DEFAULT_TARGET
    server_url = config.default_server_url

    if command == "/smoke":
        scope = "smoke"
    elif command == "/regression":
        scope = "regression"
    elif command != "/run":
        raise ValueError("Unsupported command.")

    for token in shlex.split(args_text):
        key, sep, value = token.partition("=")
        key = key.strip().lower()
        value = value.strip()

        if sep:
            if key in {"scope", "s"}:
                scope = value.lower()
            elif key in {"server", "server_url", "url"}:
                server_url = value
            elif key in {"target", "t"}:
                target = value.lower()
            else:
                raise ValueError(f"Unknown option: {key}")
            continue

        lowered = token.lower()
        if lowered in VALID_SCOPES:
            scope = lowered
        elif lowered in VALID_TARGETS:
            target = lowered
        elif lowered.startswith(("http://", "https://")):
            server_url = token
        else:
            raise ValueError(f"Unknown argument: {token}")

    scope = scope.lower()
    target = target.lower()
    server_url = normalize_url(server_url)

    if scope not in VALID_SCOPES:
        raise ValueError("Scope must be smoke or regression.")
    if target not in VALID_TARGETS:
        raise ValueError("Target must be one of: all, setup, group-a, group-b.")
    if not server_url.startswith(("http://", "https://")):
        raise ValueError("Server URL must start with http:// or https://.")
    if not config.allow_any_server and server_url not in config.allowed_server_urls:
        allowed = ", ".join(sorted(config.allowed_server_urls))
        raise ValueError(f"Server is not allowed. Allowed servers: {allowed}")

    return RunRequest(scope=scope, server_url=server_url, target=target)


def extract_message(update: dict[str, Any]) -> tuple[str, str] | None:
    message = update.get("message") or {}
    chat = message.get("chat") or {}
    chat_id = chat.get("id")
    text = message.get("text")
    if chat_id is None or not isinstance(text, str):
        return None
    return str(chat_id), text.strip()


def handle_message(
    telegram: TelegramClient,
    github: GitHubActionsClient,
    config: BotConfig,
    chat_id: str,
    text: str,
) -> None:
    command = text.split(maxsplit=1)[0].split("@", 1)[0].lower() if text else ""

    if chat_id not in config.allowed_chat_ids:
        telegram.send_message(chat_id, "This chat is not allowed to run CI.")
        return

    if command in {"/start", "/help"}:
        telegram.send_message(chat_id, help_text(config))
        return

    if command == "/servers":
        servers = "any" if config.allow_any_server else "\n".join(sorted(config.allowed_server_urls))
        telegram.send_message(chat_id, f"Allowed servers:\n{servers}")
        return

    if command not in {"/run", "/smoke", "/regression"}:
        telegram.send_message(chat_id, "Unknown command. Send /help.")
        return

    try:
        run_request = parse_run_request(text, config)
        run_url = github.dispatch(run_request)
    except Exception as exc:
        telegram.send_message(chat_id, f"Could not start tests:\n{exc}")
        return

    telegram.send_message(
        chat_id,
        (
            "GitHub Actions run started.\n"
            f"Scope: {run_request.scope}\n"
            f"Target: {run_request.target}\n"
            f"Server: {run_request.server_url}\n"
            f"Branch: {config.ref}\n"
            f"Run: {run_url}\n\n"
            "Result will be sent here when CI finishes."
        ),
    )


def main() -> int:
    try:
        config = load_config()
    except ConfigError as exc:
        print(exc, file=sys.stderr)
        return 2

    telegram = TelegramClient(config.telegram_token)
    github = GitHubActionsClient(config.github_token, config.repository, config.workflow, config.ref)

    offset: int | None = None
    print(f"Telegram CI bot started for {config.repository}/{config.workflow} on {config.ref}")

    while True:
        try:
            updates = telegram.get_updates(offset)
            for update in updates:
                update_id = update.get("update_id")
                if isinstance(update_id, int):
                    offset = update_id + 1
                extracted = extract_message(update)
                if not extracted:
                    continue
                chat_id, text = extracted
                handle_message(telegram, github, config, chat_id, text)
        except KeyboardInterrupt:
            print("Stopping Telegram CI bot.")
            return 0
        except Exception as exc:
            print(f"Bot loop error: {exc}", file=sys.stderr)
            time.sleep(5)


if __name__ == "__main__":
    raise SystemExit(main())
