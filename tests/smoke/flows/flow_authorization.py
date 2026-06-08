import os
import json
from pathlib import Path

from playwright.sync_api import Page, expect
from utils.base_page import BasePage

USER_PASS = "123456789"

DATA_STORE_PATH = Path("test-results/data/data_store.json")


def _normalize_company_code(value: str) -> str:
    return value.strip().lstrip("@")


def _create_company_enabled() -> bool:
    return os.getenv("CREATE_COMPANY", "").strip().lower() in {"1", "true", "yes", "on"}


def company_url() -> str:
    value = os.getenv("COMPANY_URL", "").strip().rstrip("/")
    if not value:
        raise AssertionError("--url majburiy. Testni scripts/run_tests.py --url <server_url> orqali ishga tushiring.")
    return value


def company_password() -> str:
    value = os.getenv("COMPANY_PASSWORD", "").strip()
    if not value:
        raise AssertionError(
            "--company-password majburiy yoki --create-company orqali yangi company admin paroli set qilingan bo'lishi kerak."
        )
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
        raise AssertionError(
            "--company-code majburiy yoki --create-company orqali yangi company yaratilgan bo'lishi kerak."
        )
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
    page.goto(f"{company_url()}/login.html")
    page.get_by_placeholder("Логин@компания").fill(email or admin_email())
    page.get_by_role("textbox", name="Пароль").fill(password or company_password())
    page.get_by_role("button", name="Войти").click()

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
