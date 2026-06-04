from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "test-results" / "allure-results"
REPORT_DIR = ROOT / "test-results" / "allure-report"
TRACE_DIR = ROOT / "test-results" / "traces"
CREATED_COMPANY_PASSWORD = "greenwhite"

TARGETS = {
    "all": ("tests/smoke/test_all_runner.py", "--new-code"),
    "setup": ("tests/smoke/test_setup/test_setup_runner.py", "--new-code"),
    "company": ("tests/smoke/test_setup/test_setup_runner.py::test_00_company", "--new-code"),
    "group-a": ("tests/smoke/test_groups/test_A_grup/test_a_group_runner.py", "--reuse-code"),
    "group-b": ("tests/smoke/test_groups/test_B_grup/test_b_group_runner.py", "--reuse-code"),
}


def normalized_url(value: str | None) -> str:
    return (value or "").strip().rstrip("/")


def clean_allure_results() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    for item in RESULTS_DIR.iterdir():
        if item.name == "history":
            continue
        if item.is_dir():
            shutil.rmtree(item, ignore_errors=True)
        else:
            item.unlink(missing_ok=True)


def command_text(command: list[str]) -> str:
    masked: list[str] = []
    hide_next = False
    for item in command:
        if hide_next:
            masked.append("***")
            hide_next = False
            continue
        masked.append(item)
        if item == "--company-password":
            hide_next = True
    return " ".join(masked)


def run(command: list[str], env: dict[str, str], dry_run: bool = False) -> int:
    print(command_text(command))
    if dry_run:
        return 0
    return subprocess.call(command, cwd=ROOT, env=env)


def generate_report(env: dict[str, str], open_report: bool, dry_run: bool) -> None:
    allure = shutil.which("allure")
    if not allure:
        return

    generate_command = [allure, "generate", str(RESULTS_DIR), "-o", str(REPORT_DIR), "--clean"]
    run(generate_command, env, dry_run=dry_run)

    if open_report:
        run([allure, "open", str(REPORT_DIR)], env, dry_run=dry_run)


def show_trace(env: dict[str, str], dry_run: bool) -> None:
    playwright = shutil.which("playwright")
    if not playwright or not TRACE_DIR.exists():
        return

    traces = sorted(TRACE_DIR.glob("*.zip"), key=lambda item: item.stat().st_mtime, reverse=True)
    if traces:
        run([playwright, "show-trace", str(traces[0])], env, dry_run=dry_run)


def parse_args() -> tuple[argparse.Namespace, list[str]]:
    parser = argparse.ArgumentParser(
        description="Smartup smoke testlarini Mac, Linux va Windows terminalida ishga tushiradi."
    )
    parser.add_argument(
        "target",
        nargs="?",
        default="all",
        help="Default: all. Debug uchun: setup, company, group-a, group-b yoki pytest target path.",
    )
    parser.add_argument("--url", required=True, help="Majburiy server URL. Masalan: https://app3.greenwhite.uz/xtrade")
    parser.add_argument("--company-code", help="Mavjud company code. --create-company bo'lmasa majburiy.")
    parser.add_argument("--company-password", help="Mavjud company admin paroli. --create-company bo'lmasa majburiy.")
    parser.add_argument(
        "--create-company",
        action="store_true",
        help="Suite boshida yangi company yaratadi va keyingi testlarda shu company_code ishlatiladi.",
    )
    parser.add_argument("--headless", action="store_true", help="Chromium headless rejimda ishlaydi.")
    parser.add_argument("--regression", action="store_true", help="SCOPE=regression bilan run qiladi.")
    parser.add_argument("--scope", choices=("smoke", "regression"), help="Test scope. Default: smoke.")
    parser.add_argument(
        "--disable-license-policy",
        action="store_true",
        help="--create-company bilan company Security tabidagi 'Политика лицензирования'ni o'chiradi.",
    )
    parser.add_argument("--open-report", action="store_true", help="Allure reportni generate qilib ochadi.")
    parser.add_argument("--show-trace", action="store_true", help="Oxirgi Playwright trace viewerini ochadi.")
    parser.add_argument("--dry-run", action="store_true", help="Commandni ko'rsatadi, lekin ishga tushirmaydi.")
    return parser.parse_known_args()


def main() -> int:
    args, pytest_extra = parse_args()
    env = os.environ.copy()

    company_url_arg = normalized_url(args.url)
    if not company_url_arg:
        print("--url bo'sh bo'lishi mumkin emas", file=sys.stderr)
        return 2
    env["COMPANY_URL"] = company_url_arg

    if args.disable_license_policy and not args.create_company:
        print("--disable-license-policy faqat --create-company bilan ishlaydi", file=sys.stderr)
        return 2
    if args.create_company and args.target in {"group-a", "group-b"}:
        print("--create-company group-a/group-b targetlari bilan ishlamaydi; all, setup yoki company ishlating", file=sys.stderr)
        return 2
    if args.target == "company" and not args.create_company:
        print("company target faqat --create-company bilan ishlaydi", file=sys.stderr)
        return 2

    if args.create_company:
        if args.company_code or args.company_password:
            print("--create-company bilan --company-code/--company-password berilmaydi", file=sys.stderr)
            return 2
        env["CREATE_COMPANY"] = "1"
        env["COMPANY_PASSWORD"] = CREATED_COMPANY_PASSWORD
        env.pop("COMPANY_CODE", None)
    else:
        company_code = (args.company_code or "").strip().lstrip("@")
        company_password = (args.company_password or "").strip()
        if not company_code:
            print("--company-code majburiy yoki --create-company flagini bering", file=sys.stderr)
            return 2
        if not company_password:
            print("--company-password majburiy yoki --create-company flagini bering", file=sys.stderr)
            return 2
        env["COMPANY_CODE"] = company_code
        env["COMPANY_PASSWORD"] = company_password
        env.pop("CREATE_COMPANY", None)

    if args.disable_license_policy:
        env["DISABLE_LICENSE_POLICY"] = "1"
    else:
        env.pop("DISABLE_LICENSE_POLICY", None)

    scope = args.scope or ("regression" if args.regression else env.get("SCOPE", "smoke"))
    if scope not in {"smoke", "regression"}:
        print(f"Unsupported scope: {scope}. Use smoke or regression.", file=sys.stderr)
        return 2

    target, code_mode = TARGETS.get(args.target, (args.target, ""))
    pytest_command = [sys.executable, "-m", "pytest", target]

    if code_mode:
        pytest_command.append(code_mode)
    if args.headless or env.get("HEADLESS", "").lower() in {"1", "true", "yes", "on"}:
        pytest_command.append("--headless")
    pytest_command.extend(["--scope", scope])
    pytest_command.extend(["--url", company_url_arg])
    if args.create_company:
        pytest_command.append("--create-company")
    else:
        pytest_command.extend(["--company-code", env["COMPANY_CODE"]])
        pytest_command.extend(["--company-password", env["COMPANY_PASSWORD"]])
    if args.disable_license_policy:
        pytest_command.append("--disable-license-policy")
    pytest_command.extend(pytest_extra)

    if args.create_company:
        print(f"Company setup: enabled by --create-company ({company_url_arg})")
        print(f"New company password: {CREATED_COMPANY_PASSWORD}")
        if args.disable_license_policy:
            print("Company license policy: will be disabled")
    else:
        print(f"Company setup: skipped; using company_code={env['COMPANY_CODE']}")

    if not args.dry_run:
        clean_allure_results()
    test_exit = run(pytest_command, env, dry_run=args.dry_run)

    generate_report(env, open_report=args.open_report, dry_run=args.dry_run)
    if args.show_trace:
        show_trace(env, dry_run=args.dry_run)

    return test_exit


if __name__ == "__main__":
    raise SystemExit(main())
