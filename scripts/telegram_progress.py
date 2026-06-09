from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
STATE_FILE = ROOT / "test-results" / "telegram-progress.json"
SYSTEM_SUMMARY_JSON = ROOT / "test-results" / "system-summary.json"
EVENT_PREFIX = "SMARTUP_PROGRESS "
MAX_MESSAGE_LENGTH = 3900


def env_value(name: str) -> str:
    return os.getenv(name, "").strip()


def telegram_enabled() -> bool:
    return bool(env_value("TELEGRAM_BOT_TOKEN") and env_value("TELEGRAM_CHAT_ID"))


def telegram_request(method: str, payload: dict[str, Any]) -> dict[str, Any] | None:
    if not telegram_enabled():
        return None
    token = env_value("TELEGRAM_BOT_TOKEN")
    encoded = urllib.parse.urlencode(payload).encode("utf-8")
    request = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/{method}",
        data=encoded,
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))
    except (OSError, urllib.error.URLError, json.JSONDecodeError) as exc:
        print(f"Telegram progress warning: {exc}", file=sys.stderr)
        return None
    if not isinstance(data, dict) or not data.get("ok"):
        print(f"Telegram progress warning: {data}", file=sys.stderr)
        return None
    return data


def load_state() -> dict[str, Any]:
    if not STATE_FILE.exists():
        return {}
    try:
        data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def save_state(state: dict[str, Any]) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def scope_line(scope: str) -> str:
    clean_scope = (scope or "smoke").strip().lower()
    if clean_scope == "regression":
        return "Regression scope tanlangan"
    return "Smoke scope tanlangan"


def result_line(item: dict[str, Any]) -> str:
    display = str(item.get("display") or item.get("test_id") or "unknown")
    status = str(item.get("status") or "UNKNOWN").upper()
    return f"{display} [{status}]"


def first_failed_result(state: dict[str, Any]) -> dict[str, Any]:
    for item in state.get("results", []):
        if isinstance(item, dict) and item.get("status") == "FAILED":
            return item
    return {}


def truncate_message(text: str) -> str:
    if len(text) <= MAX_MESSAGE_LENGTH:
        return text
    lines = text.splitlines()
    while lines and len("\n".join(lines) + "\n...") > MAX_MESSAGE_LENGTH:
        lines.pop(-1)
    return "\n".join(lines) + "\n..."


def render_message(state: dict[str, Any]) -> str:
    header_lines = [
        "Test boshlandi",
        scope_line(str(state.get("scope") or "smoke")),
    ]
    status = str(state.get("status") or "").strip()
    if status:
        header_lines.append(f"Status: {status}")
    current = str(state.get("current") or "").strip()
    if current:
        header_lines.append(f"Hozir: {current}")

    passed = [
        item for item in state.get("results", [])
        if isinstance(item, dict) and item.get("status") == "PASSED"
    ]
    failed = first_failed_result(state)

    passed_lines = [result_line(item) for item in passed]
    failed_lines: list[str] = []
    if failed:
        group = str(failed.get("group") or "").strip()
        runner = str(failed.get("runner") or "").strip()
        inner_test = str(failed.get("inner_test") or failed.get("display") or failed.get("title") or "").strip()
        step = str(failed.get("failed_step") or failed.get("step") or "").strip()
        error_type = str(failed.get("error_type") or "").strip()
        if group:
            failed_lines.append(f"Group: {group}")
        if runner:
            failed_lines.append(f"Runner test: {runner}")
        if inner_test:
            failed_lines.append(f"Ichki test: {inner_test}")
        if step:
            failed_lines.append(f"Step: {step}")
        if error_type:
            failed_lines.append(f"Error turi: {error_type}")

    def compose(current_passed: list[str]) -> str:
        lines = list(header_lines)
        if current_passed:
            lines.extend(["", "Passed:"])
            lines.extend(current_passed)
        if failed_lines:
            lines.extend(["", "Failed:"])
            lines.extend(failed_lines)
        return "\n".join(lines)

    message = compose(passed_lines)
    hidden_count = 0
    while len(message) > MAX_MESSAGE_LENGTH and len(passed_lines) > 5:
        passed_lines.pop(0)
        hidden_count += 1
        message = compose([f"... {hidden_count} ta oldingi passed test yashirildi", *passed_lines])

    return truncate_message(message)


def edit_progress(state: dict[str, Any]) -> None:
    message_id = state.get("message_id")
    if not message_id:
        return
    telegram_request(
        "editMessageText",
        {
            "chat_id": env_value("TELEGRAM_CHAT_ID"),
            "message_id": str(message_id),
            "text": render_message(state),
            "disable_web_page_preview": "true",
        },
    )


def command_start(args: argparse.Namespace) -> int:
    state = {
        "scope": args.scope,
        "server": args.server,
        "target": args.target,
        "status": args.status,
        "current": "",
        "results": [],
    }
    if not telegram_enabled():
        save_state(state)
        return 0

    if args.message_id:
        state["message_id"] = args.message_id
        edit_progress(state)
    else:
        data = telegram_request(
            "sendMessage",
            {
                "chat_id": env_value("TELEGRAM_CHAT_ID"),
                "text": render_message(state),
                "disable_web_page_preview": "true",
            },
        )
        result = data.get("result") if isinstance(data, dict) else None
        if isinstance(result, dict) and result.get("message_id"):
            state["message_id"] = result["message_id"]
    save_state(state)
    return 0


def command_update(args: argparse.Namespace) -> int:
    state = load_state()
    if not state:
        return 0
    if args.status:
        state["status"] = args.status
    if args.current is not None:
        state["current"] = args.current
    save_state(state)
    edit_progress(state)
    return 0


def update_from_event(state: dict[str, Any], event: dict[str, Any]) -> None:
    event_name = str(event.get("event") or "")
    display = str(event.get("display") or event.get("title") or event.get("test_id") or "unknown")
    if event_name == "started":
        state["status"] = "testlar ishlayapti"
        state["current"] = display
        return

    if event_name not in {"passed", "failed"}:
        return

    status = "PASSED" if event_name == "passed" else "FAILED"
    result = {
        "status": status,
        "display": display,
        "group": event.get("group") or "",
        "runner": event.get("runner") or "",
        "test_id": event.get("test_id") or "",
        "title": event.get("title") or "",
        "inner_test": event.get("title") or display,
        "error_type": event.get("error_type") or "",
    }
    state.setdefault("results", []).append(result)
    state["current"] = "" if event_name == "passed" else display


def failed_details_from_system_summary() -> dict[str, str]:
    if not SYSTEM_SUMMARY_JSON.exists():
        return {}
    try:
        data = json.loads(SYSTEM_SUMMARY_JSON.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    failed_tests = data.get("failed_tests") if isinstance(data, dict) else None
    if not isinstance(failed_tests, list) or not failed_tests:
        return {}
    first = failed_tests[0] if isinstance(failed_tests[0], dict) else {}
    return {
        "group": str(first.get("group") or ""),
        "runner": str(first.get("runner_test") or ""),
        "inner_test": str(first.get("inner_test") or ""),
        "failed_step": str(first.get("failed_step") or ""),
        "error_type": str(first.get("error_type") or ""),
    }


def enrich_failed_result_from_summary(state: dict[str, Any]) -> None:
    details = failed_details_from_system_summary()
    if not details:
        return
    for item in state.get("results", []):
        if isinstance(item, dict) and item.get("status") == "FAILED":
            item.update({key: value for key, value in details.items() if value})
            return
    state.setdefault("results", []).append(
        {
            "status": "FAILED",
            "display": details.get("inner_test") or "unknown",
            **{key: value for key, value in details.items() if value},
        }
    )


def command_run(args: argparse.Namespace) -> int:
    command = args.command
    if not command:
        print("telegram_progress.py run: command is required", file=sys.stderr)
        return 2

    state = load_state()
    process = subprocess.Popen(
        command,
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )
    assert process.stdout is not None
    for line in process.stdout:
        print(line, end="")
        if not line.startswith(EVENT_PREFIX):
            continue
        try:
            event = json.loads(line[len(EVENT_PREFIX):])
        except json.JSONDecodeError:
            continue
        if not isinstance(event, dict):
            continue
        update_from_event(state, event)
        save_state(state)
        edit_progress(state)

    exit_code = process.wait()
    if exit_code:
        enrich_failed_result_from_summary(state)
        save_state(state)
        edit_progress(state)
    return exit_code


def command_delete(_args: argparse.Namespace) -> int:
    state = load_state()
    message_id = state.get("message_id")
    if message_id and telegram_enabled():
        telegram_request(
            "deleteMessage",
            {
                "chat_id": env_value("TELEGRAM_CHAT_ID"),
                "message_id": str(message_id),
            },
        )
    STATE_FILE.unlink(missing_ok=True)
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Telegram progress message helper for GitHub Actions smoke runs.")
    subparsers = parser.add_subparsers(dest="action", required=True)

    start = subparsers.add_parser("start")
    start.add_argument("--scope", required=True)
    start.add_argument("--server", required=True)
    start.add_argument("--target", required=True)
    start.add_argument("--status", default="requirements o'rnatilyapti")
    start.add_argument("--message-id", default="")

    update = subparsers.add_parser("update")
    update.add_argument("--status", default="")
    update.add_argument("--current")

    run = subparsers.add_parser("run")
    run.add_argument("command", nargs=argparse.REMAINDER)

    subparsers.add_parser("delete")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.action == "start":
        return command_start(args)
    if args.action == "update":
        return command_update(args)
    if args.action == "run":
        if args.command and args.command[0] == "--":
            args.command = args.command[1:]
        return command_run(args)
    if args.action == "delete":
        return command_delete(args)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
