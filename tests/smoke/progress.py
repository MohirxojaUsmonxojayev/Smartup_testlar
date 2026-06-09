from __future__ import annotations

import json
from contextlib import contextmanager
from typing import Iterator

import allure


EVENT_PREFIX = "SMARTUP_PROGRESS "


def _emit_progress_event(payload: dict[str, str]) -> None:
    print(EVENT_PREFIX + json.dumps(payload, ensure_ascii=False, sort_keys=True), flush=True)


@contextmanager
def progress_step(
    *,
    group: str,
    runner: str,
    test_id: str,
    title: str,
    display: str | None = None,
) -> Iterator[None]:
    shown_name = display or title or test_id
    base_payload = {
        "group": group,
        "runner": runner,
        "test_id": test_id,
        "title": title,
        "display": shown_name,
    }
    _emit_progress_event({"event": "started", **base_payload})
    try:
        with allure.step(title):
            yield
    except Exception as exc:
        message = str(exc).splitlines()[0] if str(exc).strip() else type(exc).__name__
        _emit_progress_event(
            {
                "event": "failed",
                "error_type": type(exc).__name__,
                "message": message,
                **base_payload,
            }
        )
        raise
    else:
        _emit_progress_event({"event": "passed", **base_payload})
