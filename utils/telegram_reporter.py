"""
pytest plugin — test run tugaganda natijalarni Telegram'ga yuboradi.

SmartupAuto regression testlar uchun moslashtirilgan.
Ishlatish: tests/regression/conftest.py da quyidagicha qo'shing:
    from utils.telegram_reporter import TelegramReporter
    def pytest_configure(config):
        config.pluginmanager.register(TelegramReporter(), "telegram_reporter")
"""
import os
import re
import time
from datetime import datetime

from utils.telegram_sender import send_telegram

_final_results: dict = {}
_call_counts: dict = {}
_start_time: float = 0.0
_session_soft_failures: list = []


class TelegramReporter:

    def pytest_sessionstart(self, session) -> None:
        global _start_time
        _session_soft_failures.clear()
        _start_time = time.time()
        server = os.getenv("COMPANY_URL", "app3.greenwhite.uz/xtrade")
        send_telegram(
            "🚀 <b>Testlar boshlandi</b>\n"
            f"🌐 Server: <b>{server}</b>\n"
            f"🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )

    def pytest_runtest_logreport(self, report) -> None:
        if report.when != "call":
            return

        nodeid = report.nodeid
        raw_name = nodeid.split("::")[-1]
        name = re.sub(r'\[.*?\]$', '', raw_name).strip()

        _call_counts[nodeid] = _call_counts.get(nodeid, 0) + 1
        attempt = _call_counts[nodeid]

        if getattr(report, 'outcome', '') == 'rerun':
            return

        if report.passed:
            _final_results[nodeid] = (name, "passed", [], attempt)
        elif report.failed:
            errors = _extract_errors(report.longrepr)
            _final_results[nodeid] = (name, "failed", errors, attempt)
        elif report.skipped:
            reason = ""
            if report.longrepr and isinstance(report.longrepr, tuple):
                reason = str(report.longrepr[2]).replace("Skipped: ", "").strip()
            _final_results[nodeid] = (name, "skipped", [reason] if reason else [], attempt)

    def pytest_sessionfinish(self, session, exitstatus) -> None:
        elapsed = time.time() - (_start_time or time.time())
        _send_summary(elapsed)


def _extract_errors(longrepr) -> list:
    if not longrepr:
        return []
    text = str(longrepr).strip()

    # Allure step xatosi: qaysi stepda to'xtadi
    for line in reversed(text.splitlines()):
        stripped = line.strip()
        if "AssertionError" in stripped or stripped.startswith("E "):
            cleaned = re.sub(r'^E\s+', '', stripped)
            return [(cleaned[:300] + "…") if len(cleaned) > 300 else cleaned]

    lines = text.splitlines()
    last = lines[-1].strip() if lines else ""
    return [(last[:300] + "…") if len(last) > 300 else last] if last else []


def _send_summary(elapsed: float) -> None:
    mins = int(elapsed // 60)
    secs = int(elapsed % 60)
    now  = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    server = os.getenv("COMPANY_URL", "app3.greenwhite.uz/xtrade")

    results = list(_final_results.values())
    passed  = [r for r in results if r[1] == "passed"]
    failed  = [r for r in results if r[1] == "failed"]
    skipped = [r for r in results if r[1] == "skipped"]
    total   = len(results)

    soft_failures = list(_session_soft_failures)
    hard_failed   = bool(failed)
    soft_failed   = bool(soft_failures)

    if hard_failed or soft_failed:
        verdict = "❌ XATOLIKLAR BOR"
    else:
        verdict = "✅ MUVAFFAQIYATLI"

    lines = [
        f"📊 <b>REGRESSION TEST — {verdict}</b>",
        f"🌐 {server}",
        f"📅 {now}",
        f"⏱ {mins}m {secs}s",
        f"📦 Jami: {total}  |  ✅ {len(passed)}  |  ❌ {len(failed)}  |  ⚠️ {len(skipped)}",
        "",
    ]

    for item in results:
        name, status, errors = item[0], item[1], item[2]
        attempt = item[3] if len(item) > 3 else 1

        if status == "passed" and soft_failed:
            lines.append(f"📋 <code>{name}</code> — ⚠️ SOFT XATOLAR")
        elif status == "passed":
            note = f" <i>({attempt}-urinishda)</i>" if attempt > 1 else ""
            lines.append(f"📋 <code>{name}</code> — ✅ PASSED{note}")
        elif status == "failed":
            note = f" <i>({attempt} urinishdan keyin)</i>" if attempt > 1 else ""
            lines.append(f"📋 <code>{name}</code> — ❌ FAILED{note}")
            for err in errors[:5]:
                if err:
                    lines.append(f"   └ {err}")
        elif status == "skipped":
            lines.append(f"📋 <code>{name}</code> — ⚠️ SKIPPED")

    if total == 0:
        lines.append("⚠️ Hech qanday test natijasi aniqlanmadi.")

    if soft_failures:
        count = len(soft_failures)
        lines.append("")
        lines.append(f"⚠️ O'TMAGAN QADAMLAR ({count} ta):")
        for err in soft_failures[:10]:
            lines.append(err)
        if count > 10:
            lines.append(f"... va yana {count - 10} ta (Allure reportda ko'ring)")

    send_telegram("\n".join(lines))
