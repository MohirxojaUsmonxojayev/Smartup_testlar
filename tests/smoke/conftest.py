import os
import json
import shutil
import socket
import random
import allure
import pytest
from pathlib import Path
from typing import Any, Generator
from playwright.sync_api import sync_playwright, Browser, Page, expect
from tests.smoke.flows.flow_authorization import authorization_user
from utils.logger import write_failure_log, get_logger, TestLogger

TRACE_DIR = "test-results/traces"
DATA_DIR = "test-results/data"
ALLURE_RESULTS_DIR = "test-results/allure-results"
ALLURE_REPORT_DIR = "test-results/allure-report"
PRODUCTION_COMPANY_URL = "https://smartup.online"

# Timeout konstantalari — bitta joyda, butun loyiha bo'ylab ishlatiladi
DEFAULT_TIMEOUT    = 10_000    # click, fill, expect va boshqa locator amallari (ms)
NAVIGATION_TIMEOUT = 60_000    # page.goto, wait_for_load_state (ms)

_USER_SETUP_FAILED = False
_FAILED_SMOKE_GROUPS: set[str] = set()


def _env_flag(name: str) -> bool:
    return os.getenv(name, "").lower() in {"1", "true", "yes", "on"}


def _normalized_url(value: str | None) -> str:
    return (value or "").strip().rstrip("/")


def _is_production_company_url() -> bool:
    return _normalized_url(os.getenv("COMPANY_URL")) == PRODUCTION_COMPANY_URL


def _company_setup_enabled(config) -> bool:
    return bool(_normalized_url(os.getenv("COMPANY_URL"))) and not _is_production_company_url()


def _smoke_relative_path(path: Path, root: Path) -> Path | None:
    try:
        rel = path.resolve().relative_to(root.resolve())
    except ValueError:
        return None
    return rel if rel.parts[:2] == ("tests", "smoke") else None


def _explicit_file_args(config) -> list[Path]:
    root = Path(str(config.rootpath))
    result = []
    for raw_arg in getattr(config.invocation_params, "args", ()) or ():
        if raw_arg.startswith("-"):
            continue
        path_text = raw_arg.split("::", 1)[0]
        if not path_text:
            continue
        path = Path(path_text)
        if not path.is_absolute():
            path = root / path
        if path.is_file():
            result.append(path.resolve())
    return result


def _selected_runner_paths(config) -> set[Path]:
    root = Path(str(config.rootpath))
    raw_args = [arg for arg in (getattr(config.invocation_params, "args", ()) or ()) if not arg.startswith("-")]
    if not raw_args:
        return {(root / "tests/smoke/test_all_runner.py").resolve()}

    selected: set[Path] = set()
    for raw_arg in raw_args:
        path_text = raw_arg.split("::", 1)[0]
        path = Path(path_text)
        if not path.is_absolute():
            path = root / path
        if not path.is_dir():
            continue
        all_runner = path / "test_all_runner.py"
        if all_runner.exists():
            return {all_runner.resolve()}
        selected.update(runner.resolve() for runner in path.rglob("test_*_runner.py"))
    return selected


def pytest_addoption(parser):
    smoke = parser.getgroup("smartup smoke")
    smoke.addoption("--headless", action="store_true", default=False, help="Chromium ni headless rejimda ishga tushiradi")
    smoke.addoption("--new-code", action="store_true", default=False, help="Yangi 4 xonali code yaratadi")
    smoke.addoption("--reuse-code", action="store_true", default=False, help="data_store.json dagi mavjud code ni ishlatadi")
    smoke.addoption(
        "--scope",
        choices=("smoke", "regression"),
        default=os.getenv("TEST_SCOPE", "smoke").lower(),
        help="Test scope mode: smoke minimal tekshiruv, regression kengaytirilgan tekshiruv",
    )
    smoke.addoption(
        "--include-leaf-tests",
        action="store_true",
        default=False,
        help="Directory/default collection paytida runner bo'lmagan smoke testlarni ham collect qiladi",
    )


def pytest_collection_modifyitems(config, items):
    """Directory/default collectionda faqat mos runnerlar qolsin, duplicate business flowlar yurmasin."""
    if not _company_setup_enabled(config):
        skip_company = pytest.mark.skip(
            reason="Company setup faqat production bo'lmagan COMPANY_URL bilan ishlaydi"
        )
        for item in items:
            path_name = Path(str(item.path)).name
            if path_name == "test_company.py" or item.name == "test_00_company":
                item.add_marker(skip_company)

    if config.getoption("--include-leaf-tests") or _explicit_file_args(config):
        return

    selected_runners = _selected_runner_paths(config)
    if not selected_runners:
        return

    root = Path(str(config.rootpath))
    kept = []
    deselected = []
    for item in items:
        path = Path(str(item.path)).resolve()
        smoke_rel = _smoke_relative_path(path, root)
        if smoke_rel and path.name.startswith("test_") and path not in selected_runners:
            deselected.append(item)
            continue
        kept.append(item)

    if deselected:
        config.hook.pytest_deselected(items=deselected)
        items[:] = kept


def _smoke_group_name(item) -> str | None:
    marker = item.get_closest_marker("smoke_group")
    if not marker:
        return None
    if not marker.args:
        raise pytest.UsageError("smoke_group marker group nomini talab qiladi: @pytest.mark.smoke_group('A')")
    return str(marker.args[0])


def _is_user_setup(item) -> bool:
    return item.get_closest_marker("user_setup") is not None


def _is_headless(config) -> bool:
    return config.getoption("--headless") or _env_flag("HEADLESS")


def _browser_launch_options(config) -> dict[str, Any]:
    headless = _is_headless(config)
    return {
        "headless": headless,
        "args": [] if headless else ["--start-maximized"],
    }


def _browser_context_options(config) -> dict[str, Any]:
    if _is_headless(config):
        return {"viewport": {"width": 1920, "height": 1080}}
    return {"no_viewport": True}


def _data_file(file_name="data_store") -> Path:
    return Path(DATA_DIR) / f"{file_name}.json"


def _load_data_file(file_name="data_store") -> dict[str, Any]:
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


def _write_data_file(data: dict[str, Any], file_name="data_store") -> None:
    os.makedirs(DATA_DIR, exist_ok=True)
    path = _data_file(file_name)
    tmp_path = path.with_suffix(".json.tmp")
    with tmp_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    tmp_path.replace(path)


# ----------------------------------------------------------------------------------------------------------------------

def pytest_configure(config):
    """Allure hisoboti uchun environment, categories, executor va history tayyorlaydi."""
    expect.set_options(timeout=DEFAULT_TIMEOUT)
    os.makedirs(ALLURE_RESULTS_DIR, exist_ok=True)

    # Trend uchun: oldingi hisobotdan history ko'chirish
    history_src = os.path.join(ALLURE_REPORT_DIR, "history")
    history_dst = os.path.join(ALLURE_RESULTS_DIR, "history")
    if os.path.exists(history_src):
        shutil.rmtree(history_dst, ignore_errors=True)
        try:
            shutil.copytree(history_src, history_dst, dirs_exist_ok=True)
        except FileNotFoundError:
            pass

    # Environment
    env_path = os.path.join(ALLURE_RESULTS_DIR, "environment.properties")
    with open(env_path, "w", encoding="utf-8") as f:
        f.write("Browser=Chromium\n")
        f.write(f"Browser.Headless={_is_headless(config)}\n")
        f.write(f"Test.Scope={config.getoption('--scope')}\n")
        f.write("Framework=Playwright\n")
        f.write("Language=Python 3.11\n")
        f.write("Environment=Staging\n")
        f.write(f"Host={socket.gethostname()}\n")

    # Categories
    categories_src = "allure/categories.json"
    categories_dst = os.path.join(ALLURE_RESULTS_DIR, "categories.json")
    if os.path.exists(categories_src):
        shutil.copy(categories_src, categories_dst)

    # Executor
    executor_path = os.path.join(ALLURE_RESULTS_DIR, "executor.json")
    executor_data = {
        "name": socket.gethostname(),
        "type": "local",
        "buildName": "Smoke Tests",
        "reportName": "Allure Report"
    }
    with open(executor_path, "w", encoding="utf-8") as f:
        json.dump(executor_data, f, indent=2)

# ----------------------------------------------------------------------------------------------------------------------

@pytest.fixture
def browser(request):
    """Bitta browser instance, to'liq ekranda ochiladi."""
    with sync_playwright() as p:
        browser_obj = p.chromium.launch(**_browser_launch_options(request.config))
        yield browser_obj
        browser_obj.close()

# ----------------------------------------------------------------------------------------------------------------------

@pytest.fixture(scope="session")
def session_browser(request):
    """Butun sessiya uchun bitta browser (setup/group runnerlar uchun)."""
    with sync_playwright() as p:
        browser_obj = p.chromium.launch(**_browser_launch_options(request.config))
        yield browser_obj
        browser_obj.close()

# ----------------------------------------------------------------------------------------------------------------------

@pytest.fixture(scope="session")
def session_context(session_browser, request):
    """Barcha smoke testlar uchun yagona context. Bitta trace yoziladi."""
    context = session_browser.new_context(**_browser_context_options(request.config))
    context.set_default_timeout(DEFAULT_TIMEOUT)
    context.set_default_navigation_timeout(NAVIGATION_TIMEOUT)
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield context
    os.makedirs(TRACE_DIR, exist_ok=True)
    context.tracing.stop(path=os.path.join(TRACE_DIR, "smoke_trace.zip"))
    context.close()

# ----------------------------------------------------------------------------------------------------------------------

@pytest.fixture(scope="session")
def session_page(session_context) -> Generator[Page, Any, None]:
    """Barcha smoke testlar uchun yagona sahifa — holat saqlanadi."""
    page_obj = session_context.new_page()
    yield page_obj
    page_obj.close()

# ----------------------------------------------------------------------------------------------------------------------

@pytest.fixture
def group_page(session_browser: Browser, request) -> Generator[Page, Any, None]:
    """Group testlar uchun fresh context/page. Grouplar bir-birining UI holatini meros qilmaydi."""
    context = session_browser.new_context(**_browser_context_options(request.config))
    context.set_default_timeout(DEFAULT_TIMEOUT)
    context.set_default_navigation_timeout(NAVIGATION_TIMEOUT)
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    page_obj = context.new_page()

    yield page_obj

    os.makedirs(TRACE_DIR, exist_ok=True)
    safe_name = request.node.nodeid.replace("/", "_").replace("::", "__")
    context.tracing.stop(path=os.path.join(TRACE_DIR, f"{safe_name}.zip"))
    page_obj.close()
    context.close()

# ----------------------------------------------------------------------------------------------------------------------

@pytest.fixture(scope="module")
def group_session_page(session_browser: Browser, request, code) -> Generator[Page, Any, None]:
    """Bitta group runner moduli uchun bitta context/page."""
    context = session_browser.new_context(**_browser_context_options(request.config))
    context.set_default_timeout(DEFAULT_TIMEOUT)
    context.set_default_navigation_timeout(NAVIGATION_TIMEOUT)
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    page_obj = context.new_page()

    yield page_obj

    os.makedirs(TRACE_DIR, exist_ok=True)
    safe_name = request.module.__name__.replace(".", "_")
    context.tracing.stop(path=os.path.join(TRACE_DIR, f"{safe_name}.zip"))
    page_obj.close()
    context.close()


@pytest.fixture(scope="module")
def group_user_page(group_session_page: Page, code: str) -> Page:
    """Group boshida user sifatida bir marta login qiladi."""
    authorization_user(group_session_page, code)
    expect(group_session_page.get_by_role("heading", name="Trade")).to_be_visible()
    return group_session_page

# ----------------------------------------------------------------------------------------------------------------------

@pytest.fixture
def page(browser: Browser, request) -> Generator[Page, Any, None]:
    """Har bir test uchun yangi sahifa, to'liq ekran (no_viewport + --start-maximized). Trace yoziladi."""
    context = browser.new_context(**_browser_context_options(request.config))
    context.set_default_timeout(DEFAULT_TIMEOUT)
    context.set_default_navigation_timeout(NAVIGATION_TIMEOUT)

    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    page_obj = context.new_page()

    yield page_obj

    os.makedirs(TRACE_DIR, exist_ok=True)
    safe_name = request.node.nodeid.replace("/", "_").replace("::", "__")
    context.tracing.stop(path=os.path.join(TRACE_DIR, f"{safe_name}.zip"))
    page_obj.close()
    context.close()

# ----------------------------------------------------------------------------------------------------------------------

@pytest.fixture(scope="session")
def test_scope(request) -> str:
    """Global test scope: smoke yoki regression."""
    return request.config.getoption("--scope")

# ----------------------------------------------------------------------------------------------------------------------

@pytest.fixture(scope="session")
def company_setup_enabled(request) -> bool:
    """Company setup non-production COMPANY_URL bilan yoqilgan-yoqilmaganini qaytaradi."""
    return _company_setup_enabled(request.config)

# ----------------------------------------------------------------------------------------------------------------------

@pytest.fixture(scope="session")
def code(request):
    """
    user_setup runner orqali ishlaganda: yangi random code yaratadi.
    Yakka test ishlaganda: data_store.json fayldan o'qiydi.
    """
    if request.config.getoption("--new-code") and request.config.getoption("--reuse-code"):
        raise pytest.UsageError("--new-code va --reuse-code birga ishlatilmaydi")

    is_full_run = request.config.getoption("--new-code") or (
        not request.config.getoption("--reuse-code")
        and any(_is_user_setup(item) for item in request.session.items)
    )

    if is_full_run:
        return str(random.randint(1000, 9999))

    saved = _load_data_file().get("code")
    if saved:
        return saved

    pytest.exit("Yakka test uchun saqlangan 'code' topilmadi. Avval test_setup_runner ni ishga tushiring.")

# ----------------------------------------------------------------------------------------------------------------------

@pytest.fixture(scope="session")
def save_data():
    """JSON faylga ma'lumot saqlash."""
    os.makedirs(DATA_DIR, exist_ok=True)

    def _save(key, value, file_name="data_store"):
        data = _load_data_file(file_name)
        data[key] = value
        _write_data_file(data, file_name)

    return _save

# ----------------------------------------------------------------------------------------------------------------------

@pytest.fixture(scope="session")
def load_data():
    """JSON fayldan ma'lumot o'qish."""
    def _load(key, file_name="data_store"):
        return _load_data_file(file_name).get(key)

    return _load

# ----------------------------------------------------------------------------------------------------------------------

@pytest.fixture(scope="session")
def require_data(load_data):
    """JSON dan majburiy key o'qish; yo'q bo'lsa timeout emas, aniq xato beradi."""
    def _require(key, file_name="data_store"):
        value = load_data(key, file_name=file_name)
        if value in (None, ""):
            raise AssertionError(f"{file_name}.json ichida majburiy key topilmadi: {key}")
        return value

    return _require

# ----------------------------------------------------------------------------------------------------------------------

@pytest.fixture
def logger(request) -> Generator[TestLogger, Any, None]:
    """Har bir test funksiyasi uchun alohida logger fixture."""
    test_logger = get_logger(request.node.nodeid)
    yield test_logger
    test_logger.close()

# ----------------------------------------------------------------------------------------------------------------------

def pytest_runtest_setup(item):
    """User setup va smoke group dependency skip mexanizmi."""
    if _is_user_setup(item) and _USER_SETUP_FAILED:
        pytest.skip("Oldingi user_setup testi failed bo'lgani uchun qolgan user_setup testlari skip qilindi")

    group_name = _smoke_group_name(item)
    if not group_name:
        return

    if _USER_SETUP_FAILED:
        pytest.skip("User setup failed bo'lgani uchun barcha group testlar skip qilindi")

    if group_name in _FAILED_SMOKE_GROUPS:
        pytest.skip(f"{group_name} group ichidagi oldingi test failed bo'lgani uchun skip qilindi")

# ----------------------------------------------------------------------------------------------------------------------

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Test xato bo'lganda screenshot olib Allure ga qo'shadi."""
    global _USER_SETUP_FAILED
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = (
            item.funcargs.get("session_page")
            or item.funcargs.get("group_user_page")
            or item.funcargs.get("group_session_page")
            or item.funcargs.get("group_page")
            or item.funcargs.get("page")
        )
        if page:
            try:
                allure.attach(page.url, name="current-url", attachment_type=allure.attachment_type.TEXT)
                allure.attach(page.title(), name="page-title", attachment_type=allure.attachment_type.TEXT)
                screenshot = page.screenshot(full_page=True)
                allure.attach(
                    screenshot,
                    name="screenshot",
                    attachment_type=allure.attachment_type.PNG,
                )
            except Exception as exc:
                allure.attach(str(exc), name="failure-hook-error", attachment_type=allure.attachment_type.TEXT)

        data_path = _data_file()
        if data_path.exists():
            allure.attach(
                data_path.read_text(encoding="utf-8"),
                name="data-store",
                attachment_type=allure.attachment_type.JSON,
            )

    if report.failed:
        if _is_user_setup(item):
            _USER_SETUP_FAILED = True

        group_name = _smoke_group_name(item)
        if group_name:
            _FAILED_SMOKE_GROUPS.add(group_name)

# ----------------------------------------------------------------------------------------------------------------------

def pytest_runtest_logreport(report: pytest.TestReport) -> None:
    """
    Har bir test fazasi (setup / call / teardown) tugaganda chaqiriladi.
    Agar test muvaffaqiyatsiz bo'lsa, test-results/logs/ ichiga log yozadi.
    """
    if report.failed:
        longrepr_str = str(report.longrepr) if report.longrepr else "Xabar yo'q"
        log_path = write_failure_log(report.nodeid, report.when, longrepr_str)
        print(f"\n[LOG] Xato logi saqlandi: {log_path}")

# ----------------------------------------------------------------------------------------------------------------------
