import os
import json
from pathlib import Path

from dotenv import load_dotenv
from playwright.sync_api import Page, expect
from utils.base_page import BasePage

load_dotenv()

COMPANY_URL = os.environ["COMPANY_URL"]
COMPANY_CODE = os.environ["COMPANY_CODE"]
COMPANY_PASS = os.environ["COMPANY_PASSWORD"]
USER_PASS = os.environ["USER_PASSWORD"]

DATA_STORE_PATH = Path("test-results/data/data_store.json")


def _normalize_company_code(value: str) -> str:
    return value.strip().lstrip("@")


def current_company_code() -> str:
    if DATA_STORE_PATH.exists():
        try:
            data = json.loads(DATA_STORE_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            data = {}
        company_code = data.get("company_code") if isinstance(data, dict) else None
        if company_code:
            return _normalize_company_code(str(company_code))
    return _normalize_company_code(COMPANY_CODE)


def company_suffix() -> str:
    return f"@{current_company_code()}"


def admin_email() -> str:
    return f"admin{company_suffix()}"


def user_email_for(code: str) -> str:
    return f"user-pw{code}{company_suffix()}"


ADMIN_EMAIL = admin_email()

# ----------------------------------------------------------------------------------------------------------------------

def logout(page: Page) -> None:
    page.locator(".btn.btn-icon.w-auto").click()
    expect(page.locator("#kt_header").get_by_text("Admin")).to_be_visible()
    page.locator('a[ng-click="a.logout()"]').click()
    BasePage(page).confirm_biruni("Хотите выйти?")

# ----------------------------------------------------------------------------------------------------------------------

def login(page: Page, email: str | None = None, password: str = COMPANY_PASS) -> None:
    page.goto(f"{COMPANY_URL}/login.html")
    page.get_by_placeholder("Логин@компания").fill(email or admin_email())
    page.get_by_role("textbox", name="Пароль").fill(password)
    page.get_by_role("button", name="Войти").click()

# ----------------------------------------------------------------------------------------------------------------------

def dashboard(page: Page) -> None:
    expect(page.get_by_role("heading", name="Trade")).to_be_visible(timeout=120_000)

# ----------------------------------------------------------------------------------------------------------------------

def authorization(page: Page, email: str | None = None, password: str = COMPANY_PASS) -> None:
    login(page, email=email, password=password)
    dashboard(page)

# ----------------------------------------------------------------------------------------------------------------------

def authorization_user(page: Page, code: str) -> None:
    login(page, email=user_email_for(code), password=USER_PASS)
    dashboard(page)

# ----------------------------------------------------------------------------------------------------------------------
