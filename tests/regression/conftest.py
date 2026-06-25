import json
import os
import random
import shutil
import socket

import allure
import pytest
from pathlib import Path
from typing import Any, Generator
from playwright.sync_api import sync_playwright, Browser, Page, expect

from utils.logger import write_failure_log, get_logger, TestLogger
from utils.telegram_reporter import TelegramReporter
from utils.soft_assert import SoftAssert

TRACE_DIR = "test-results/traces"
DATA_DIR = "test-results/data"
ALLURE_RESULTS_DIR = "test-results/allure-results"
ALLURE_REPORT_DIR = "test-results/allure-report"

DEFAULT_TIMEOUT    = 120_000
NAVIGATION_TIMEOUT = 120_000


def _env_flag(name: str) -> bool:
    return os.getenv(name, "").lower() in {"1", "true", "yes", "on"}


def _normalized_url(value: str | None) -> str:
    return (value or "").strip().rstrip("/")


def _is_headless(config) -> bool:
    return config.getoption("--headless") or _env_flag("HEADLESS")


def _browser_launch_options(config) -> dict[str, Any]:
    headless = _is_headless(config)
    return {
        "headless": headless,
        "args": [] if headless else ["--start-maximized"],
    }


def _browser_context_options(config) -> dict[str, Any]:
    options: dict[str, Any] = {"accept_downloads": True}
    if _is_headless(config):
        options["viewport"] = {"width": 1920, "height": 1080}
    else:
        options["no_viewport"] = True
    return options


# ----------------------------------------------------------------------------------------------------------------------

def pytest_addoption(parser):
    group = parser.getgroup("smartup regression")
    group.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Chromium ni headless rejimda ishga tushiradi",
    )
    group.addoption(
        "--url",
        default="",
        help="Majburiy SmartupERP server URL. Masalan: --url https://app.smartup.uz/xtrade",
    )
    group.addoption(
        "--company-code",
        default="",
        help="Company kodi (@ belgisisiz). Masalan: --company-code novatrade",
    )
    group.addoption(
        "--company-password",
        default="",
        help="Company admin paroli",
    )
    group.addoption(
        "--scope",
        choices=("smoke", "regression"),
        default=os.getenv("TEST_SCOPE", "regression").lower(),
        help="Test scope: smoke yoki regression",
    )
    group.addoption(
        "--new-code",
        action="store_true",
        default=False,
        help="Yangi tasodifiy code yaratadi va data_store.json ga saqlaydi",
    )
    group.addoption(
        "--reuse-code",
        action="store_true",
        default=False,
        help="data_store.json dagi mavjud code ni ishlatadi (alohida test ishlatganda)",
    )


# ----------------------------------------------------------------------------------------------------------------------

def pytest_configure(config):
    config.pluginmanager.register(TelegramReporter(), "telegram_reporter")

    expect.set_options(timeout=DEFAULT_TIMEOUT)

    company_url = _normalized_url(config.getoption("--url"))
    if not company_url:
        raise pytest.UsageError(
            "--url majburiy. Masalan: --url https://app.smartup.uz/xtrade"
        )
    os.environ["COMPANY_URL"] = company_url

    company_code = str(config.getoption("--company-code") or "").strip().lstrip("@")
    if not company_code:
        raise pytest.UsageError("--company-code majburiy. Masalan: --company-code novatrade")
    os.environ["COMPANY_CODE"] = company_code

    company_password = str(config.getoption("--company-password") or "").strip()
    if not company_password:
        raise pytest.UsageError("--company-password majburiy.")
    os.environ["COMPANY_PASSWORD"] = company_password

    os.makedirs(ALLURE_RESULTS_DIR, exist_ok=True)

    history_src = os.path.join(ALLURE_REPORT_DIR, "history")
    history_dst = os.path.join(ALLURE_RESULTS_DIR, "history")
    if os.path.exists(history_src):
        shutil.rmtree(history_dst, ignore_errors=True)
        try:
            shutil.copytree(history_src, history_dst, dirs_exist_ok=True)
        except FileNotFoundError:
            pass

    env_path = os.path.join(ALLURE_RESULTS_DIR, "environment.properties")
    with open(env_path, "w", encoding="utf-8") as f:
        f.write("Browser=Chromium\n")
        f.write(f"Browser.Headless={_is_headless(config)}\n")
        f.write(f"Test.Scope={config.getoption('--scope')}\n")
        f.write(f"Company.URL={company_url}\n")
        f.write(f"Company.Code={company_code}\n")
        f.write("Framework=Playwright\n")
        f.write("Language=Python 3.11\n")
        f.write("Environment=Regression\n")
        f.write(f"Host={socket.gethostname()}\n")


# ----------------------------------------------------------------------------------------------------------------------
# Data store yordamchi funksiyalari

def _data_file(file_name: str = "data_store") -> Path:
    return Path(DATA_DIR) / f"{file_name}.json"


def _load_data_file(file_name: str = "data_store") -> dict[str, Any]:
    path = _data_file(file_name)
    if not path.exists():
        return {}
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as exc:
        raise AssertionError(f"{path} buzilgan JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise AssertionError(f"{path} ichida JSON object bo'lishi kerak")
    return data


def _write_data_file(data: dict[str, Any], file_name: str = "data_store") -> None:
    os.makedirs(DATA_DIR, exist_ok=True)
    path = _data_file(file_name)
    tmp_path = path.with_suffix(".json.tmp")
    with tmp_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    tmp_path.replace(path)


# ----------------------------------------------------------------------------------------------------------------------

@pytest.fixture(scope="session")
def session_browser(request):
    """Butun sessiya uchun bitta browser."""
    with sync_playwright() as p:
        browser_obj = p.chromium.launch(**_browser_launch_options(request.config))
        yield browser_obj
        browser_obj.close()


@pytest.fixture(scope="session")
def session_context(session_browser, request):
    """Sessiya uchun bitta context. Trace yoziladi."""
    context = session_browser.new_context(**_browser_context_options(request.config))
    context.set_default_timeout(DEFAULT_TIMEOUT)
    context.set_default_navigation_timeout(NAVIGATION_TIMEOUT)
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield context
    os.makedirs(TRACE_DIR, exist_ok=True)
    context.tracing.stop(path=os.path.join(TRACE_DIR, "regression_trace.zip"))
    context.close()


@pytest.fixture(scope="session")
def session_page(session_context) -> Generator[Page, Any, None]:
    """Barcha sessiya testlari uchun yagona sahifa."""
    page_obj = session_context.new_page()
    yield page_obj
    page_obj.close()


@pytest.fixture
def browser(request) -> Generator[Browser, Any, None]:
    """Har bir test uchun alohida browser."""
    with sync_playwright() as p:
        browser_obj = p.chromium.launch(**_browser_launch_options(request.config))
        yield browser_obj
        browser_obj.close()


@pytest.fixture
def page(browser: Browser, request) -> Generator[Page, Any, None]:
    """Har bir test uchun yangi sahifa. Trace yoziladi."""
    context = browser.new_context(**_browser_context_options(request.config))
    context.set_default_timeout(DEFAULT_TIMEOUT)
    context.set_default_navigation_timeout(NAVIGATION_TIMEOUT)
    context.tracing.start(screenshots=True, snapshots=False, sources=False)
    page_obj = context.new_page()

    yield page_obj

    os.makedirs(TRACE_DIR, exist_ok=True)
    safe_name = request.node.nodeid.replace("/", "_").replace("::", "__")
    trace_path = os.path.join(TRACE_DIR, f"{safe_name}.zip")

    failed = getattr(getattr(request.node, "rep_call", None), "failed", False)

    if failed:
        # FAIL: trace saqlanadi va Allure ga biriktiriladi
        context.tracing.stop(path=trace_path)
        try:
            with open(trace_path, "rb") as _tf:
                allure.attach(
                    _tf.read(),
                    name="playwright-trace.zip",
                    attachment_type="application/zip",
                    extension="zip",
                )
        except Exception:
            pass
        # Fail paytidagi sahifa screenshoti
        try:
            allure.attach(page_obj.url, name="current-url", attachment_type=allure.attachment_type.TEXT)
            screenshot = page_obj.screenshot(full_page=True)
            allure.attach(screenshot, name="screenshot-on-fail", attachment_type=allure.attachment_type.PNG)
        except Exception:
            pass
    else:
        # PASS: trace diskga saqlanmaydi (disk tejaladi)
        context.tracing.stop()
        # Yakuniy holat screenshoti (1 ta)
        try:
            screenshot = page_obj.screenshot(full_page=True)
            allure.attach(screenshot, name="final-screenshot", attachment_type=allure.attachment_type.PNG)
        except Exception:
            pass

    page_obj.close()
    context.close()


# ----------------------------------------------------------------------------------------------------------------------

@pytest.fixture(scope="session")
def test_scope(request) -> str:
    return request.config.getoption("--scope")


@pytest.fixture(scope="session")
def code(request) -> str:
    """
    Sessiya davomida barcha testlar uchun yagona unikal suffiks.

    Uch xil rejim:
      --new-code    → yangi tasodifiy 6 raqamli son yaratadi, data_store.json ga saqlaydi.
      --reuse-code  → data_store.json dan mavjud code ni o'qiydi (alohida test ishlatganda).
      (default)     → --new-code bilan bir xil: har sessiyada yangi code.

    Qoidasi: to'liq suite ishlatganda har doim yangi code,
    yakka test debug qilganda --reuse-code bilan oldingi ma'lumotlarni qayta topadi.
    """
    use_new = request.config.getoption("--new-code")
    use_reuse = request.config.getoption("--reuse-code")

    if use_new and use_reuse:
        raise pytest.UsageError("--new-code va --reuse-code birga ishlatilmaydi")

    if use_reuse:
        saved = _load_data_file().get("code")
        if not saved:
            pytest.exit(
                "data_store.json da saqlangan 'code' topilmadi. "
                "Avval to'liq suite --new-code bilan ishga tushiring."
            )
        return str(saved)

    # default yoki --new-code: yangi code yarat va saqlash
    new_code = str(random.randint(100_000, 999_999))
    _write_data_file({"code": new_code})
    return new_code


@pytest.fixture(scope="session")
def save_data():
    """JSON faylga kalit-qiymat saqlash. Testlar orasida ma'lumot uzatish uchun."""
    os.makedirs(DATA_DIR, exist_ok=True)

    def _save(key: str, value: Any, file_name: str = "data_store") -> None:
        data = _load_data_file(file_name)
        data[key] = value
        _write_data_file(data, file_name)

    return _save


@pytest.fixture(scope="session")
def load_data():
    """JSON fayldan kalit bo'yicha qiymat o'qish."""
    def _load(key: str, file_name: str = "data_store") -> Any:
        return _load_data_file(file_name).get(key)

    return _load


@pytest.fixture(scope="session")
def require_data(load_data):
    """JSON dan majburiy key o'qish — yo'q bo'lsa aniq xato beradi, timeout emas."""
    def _require(key: str, file_name: str = "data_store") -> Any:
        value = load_data(key, file_name=file_name)
        if value in (None, ""):
            raise AssertionError(
                f"'{key}' topilmadi {file_name}.json da. "
                "Avval uni saqlaydigan test ishga tushirilganmi?"
            )
        return value

    return _require


@pytest.fixture
def logger(request) -> Generator[TestLogger, Any, None]:
    """Har bir test uchun alohida logger."""
    test_logger = get_logger(request.node.nodeid)
    yield test_logger
    test_logger.close()


@pytest.fixture
def soft() -> Generator[SoftAssert, Any, None]:
    """Soft assertion — test to'xtamasdan xatolarni yig'adi, oxirida assert_all() chaqiriladi."""
    s = SoftAssert()
    yield s
    s.assert_all()


# ----------------------------------------------------------------------------------------------------------------------

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Test natijasini item.rep_<phase> ga saqlaydi; session_page FAIL screenshoti."""
    outcome = yield
    report = outcome.get_result()
    setattr(item, "rep_" + report.when, report)

    # Faqat session_page uchun screenshot — function-scoped `page` fixture
    # o'zining teardown'ida boshqaradi (pastdagi page fixture'ga qarang)
    if report.when == "call" and report.failed:
        session_page = item.funcargs.get("session_page")
        if session_page:
            try:
                allure.attach(session_page.url, name="current-url", attachment_type=allure.attachment_type.TEXT)
                allure.attach(session_page.title(), name="page-title", attachment_type=allure.attachment_type.TEXT)
                screenshot = session_page.screenshot(full_page=True)
                allure.attach(
                    screenshot,
                    name="screenshot",
                    attachment_type=allure.attachment_type.PNG,
                )
            except Exception as exc:
                allure.attach(str(exc), name="failure-hook-error", attachment_type=allure.attachment_type.TEXT)


def pytest_runtest_logreport(report: pytest.TestReport) -> None:
    if report.failed:
        longrepr_str = str(report.longrepr) if report.longrepr else "Xabar yo'q"
        log_path = write_failure_log(report.nodeid, report.when, longrepr_str)
        print(f"\n[LOG] Xato logi saqlandi: {log_path}")
