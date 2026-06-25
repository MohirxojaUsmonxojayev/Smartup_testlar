import os
import json
from pathlib import Path

from playwright.sync_api import Page, expect
from utils.base_page import BasePage

USER_PASS = "123456789"

DATA_STORE_PATH = Path("test-results/data/data_store.json")

_session_passwords: dict[int, str] = {}
_session_handler_pages: set[int] = set()


def _normalize_company_code(value: str) -> str:
    return value.strip().lstrip("@")


def _create_company_enabled() -> bool:
    return os.getenv("CREATE_COMPANY", "").strip().lower() in {"1", "true", "yes", "on"}


def company_url() -> str:
    value = os.getenv("COMPANY_URL", "").strip().rstrip("/")
    if not value:
        raise AssertionError("--url majburiy. Testni --url <server_url> orqali ishga tushiring.")
    return value


def company_password() -> str:
    value = os.getenv("COMPANY_PASSWORD", "").strip()
    if not value:
        raise AssertionError("--company-password majburiy.")
    return value


def current_company_code() -> str:
    if _create_company_enabled() and DATA_STORE_PATH.exists():
        try:
            data = json.loads(DATA_STORE_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            data = {}
        company_code = data.get("company_code") if isinstance(data, dict) else None
        if company_code:
            return _normalize_company_code(str(company_code))
    value = os.getenv("COMPANY_CODE", "").strip()
    if not value:
        raise AssertionError("--company-code majburiy.")
    return _normalize_company_code(value)


def company_suffix() -> str:
    return f"@{current_company_code()}"


def admin_email() -> str:
    return f"admin{company_suffix()}"


def user_email_for(code: str) -> str:
    return f"user-pw{code}{company_suffix()}"


# ----------------------------------------------------------------------------------------------------------------------

def logout(page: Page) -> None:
    page.locator(".btn.btn-icon.w-auto").click()
    expect(page.locator("#kt_header").get_by_text("Admin")).to_be_visible()
    page.locator('a[ng-click="a.logout()"]').click()
    BasePage(page).confirm_biruni("Хотите выйти?")

# ----------------------------------------------------------------------------------------------------------------------

def login(page: Page, email: str | None = None, password: str | None = None) -> None:
    email = email or admin_email()
    password = password or company_password()
    page.goto(f"{company_url()}/login.html")
    page.get_by_placeholder("Логин@компания").fill(email)
    page.get_by_role("textbox", name="Пароль").fill(password)
    page.get_by_role("button", name="Войти").click()
    install_session_keepalive(page, password)

# ----------------------------------------------------------------------------------------------------------------------

def install_session_keepalive(page: Page, password: str) -> None:
    """
    Smartup sessiya timeout (#closing-session) overlay chiqsa avtomatik hal qiladi.
    Timeout-warning holatida "Продолжить" bosadi; lock holatida parol kiritib qayta kiradi.
    """
    _session_passwords[id(page)] = password
    if id(page) in _session_handler_pages:
        return
    _session_handler_pages.add(id(page))

    overlay = page.locator("#closing-session")
    backdrop_open = page.locator("#closing-session .cs-backdrop.open")

    def _resolve_session_lock() -> None:
        try:
            stay = overlay.get_by_role("button", name="Продолжить")
            if stay.count() > 0 and stay.first.is_visible():
                stay.first.click()
            else:
                pwd = overlay.locator("input[type=password]").first
                if pwd.is_visible():
                    pwd.fill(_session_passwords.get(id(page), password))
                    pwd.press("Tab")
                    overlay.get_by_role("button", name="Войти", exact=True).first.click()
            backdrop_open.wait_for(state="hidden", timeout=60_000)
        except Exception:
            pass

    page.add_locator_handler(
        page.locator("#closing-session .cs-backdrop.open"),
        _resolve_session_lock,
        no_wait_after=True,
    )

# ----------------------------------------------------------------------------------------------------------------------

def dashboard(page: Page) -> None:
    expect(page.get_by_role("heading", name="Trade")).to_be_visible(timeout=120_000)

# ----------------------------------------------------------------------------------------------------------------------

def authorization(page: Page, email: str | None = None, password: str | None = None) -> None:
    login(page, email=email, password=password)
    dashboard(page)

# ----------------------------------------------------------------------------------------------------------------------

def authorization_user(page: Page, code: str) -> None:
    login(page, email=user_email_for(code), password=USER_PASS)
    dashboard(page)

# ----------------------------------------------------------------------------------------------------------------------
