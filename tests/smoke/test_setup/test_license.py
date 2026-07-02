import os
import re

import allure
from tests.smoke.flows.flow_authorization import authorization, logout
from tests.smoke.flows.flow_navigate import navigate_to, switch_filial, expect_page
from utils.base_page import BasePage
from playwright.sync_api import expect, TimeoutError as PlaywrightTimeoutError

pytestmark = [allure.epic("Smoke"), allure.feature("Setup"), allure.story("License")]

MANDATORY_LICENSE_COUNT = "5"
REGULAR_LICENSE_COUNT = "1"
MANDATORY_LICENSE_ROW_RE = re.compile(r"Smartup ERP:\s*Базовый пользователь\s*\(Обязательный\)")
REGULAR_LICENSE_ROW_RE = re.compile(r"Smartup ERP:\s*Базовый пользователь\s+За пользователя")

# ----------------------------------------------------------------------------------------------------------------------

def _env_flag(name):
    return os.getenv(name, "").strip().lower() in {"1", "true", "yes", "on"}


def _license_policy_disabled():
    return _env_flag("DISABLE_LICENSE_POLICY")


def _attach_license_skip_note(logger, step_name):
    message = (
        f"{step_name} o'tkazib yuborildi: --disable-license-policy berilgani uchun "
        "companyda Политика лицензирования o'chirilgan."
    )
    allure.attach(message, name="license-policy-disabled", attachment_type=allure.attachment_type.TEXT)
    logger.info(message)


def _logout_if_authenticated(page, logger):
    if page.locator(".btn.btn-icon.w-auto").is_visible():
        logout(page)
    else:
        logger.info("Faol sessiya topilmadi — logout o'tkazib yuborildi")


def _prepare_license_purchase(page, base_page):
    if not page.get_by_role("button", name="Купить").is_visible():
        page.get_by_role("link", name="Покупка").click()

    base_page.select_option(ng_model="purchase.payer.name", option_text="AUTOTEST GWS", clear=True)
    base_page.select_option(ng_model="purchase.contract_name", option_text="Договор № bn от 01.01.2025", clear=True)
    base_page.select_date(ng_model="purchase.begin_date", option="today")
    base_page.wait_for_loader()


def _optional_license_row(page, row_name, timeout=3_000):
    row = page.get_by_role("row", name=row_name).first
    try:
        row.wait_for(state="visible", timeout=timeout)
        return row
    except PlaywrightTimeoutError:
        return None


def _license_row(page, row_name):
    row = page.get_by_role("row", name=row_name).first
    expect(row).to_be_visible()
    return row


def _buy_license_row(
    page,
    base_page,
    row,
    count,
    logger,
    success_message,
    editable_quantity=True,
):
    if editable_quantity:
        quantity = row.get_by_role("textbox").first
        quantity.fill(count)
        expect(quantity).to_have_value(count)
    else:
        expect(page.locator("body")).to_contain_text(f"Итого лицензий: {count}")

    page.get_by_role("button", name="Купить").click()
    terms = page.locator("span").filter(has_text="Я ознакомился с тем").first
    expect(terms).to_be_visible()
    terms.click()
    page.get_by_role("button", name="Да", exact=True).click()
    base_page.wait_for_loader()
    logger.info(success_message)


# ----------------------------------------------------------------------------------------------------------------------

def run_buy_license(page, logger):
    if _license_policy_disabled():
        _attach_license_skip_note(logger, "Litsenziya sotib olish")
        return

    with allure.step("1 - Admin sifatida kirish va litsenziyalar sahifasiga o'tish"):
        _logout_if_authenticated(page, logger)
        authorization(page)
        switch_filial(page, name="Администрирование")
        navigate_to(page, tab="Главное", name="Лицензии")
        expect_page(page, heading="Лицензии")

    with allure.step("2 - Balansni tekshirish"):
        balance_locator = page.locator('p.text-success[ng-if="q.balance > 0"]')
        try:
            balance_locator.wait_for(state="visible", timeout=5_000)
            logger.info("Balans musbat — Success")
        except Exception:
            logger.fail("Balans musbat emas yoki element topilmadi!", raise_error=True)

    with allure.step("3 - Litsenziya sotib olish"):
        base_page = BasePage(page)
        _prepare_license_purchase(page, base_page)

        mandatory_row = _optional_license_row(page, MANDATORY_LICENSE_ROW_RE)
        if mandatory_row:
            with allure.step("3.1 - Majburiy bazaviy litsenziyalarni sotib olish"):
                _buy_license_row(
                    page,
                    base_page,
                    mandatory_row,
                    MANDATORY_LICENSE_COUNT,
                    logger,
                    "Majburiy bazaviy litsenziyalar olindi",
                    editable_quantity=False,
                )
                _prepare_license_purchase(page, base_page)
        else:
            logger.info("Majburiy bazaviy litsenziya bu oy uchun chiqmagan")

        with allure.step("3.2 - Oddiy bazaviy litsenziya sotib olish"):
            row = _license_row(page, REGULAR_LICENSE_ROW_RE)
            _buy_license_row(page, base_page, row, REGULAR_LICENSE_COUNT, logger, "Litsenziya olindi")

# ----------------------------------------------------------------------------------------------------------------------

def run_attach_license(page, code, logger):
    if _license_policy_disabled():
        _attach_license_skip_note(logger, "Litsenziyani foydalanuvchiga ulash")
        return

    with allure.step("1 - Litsenziyalar va hujjatlar sahifasiga o'tish"):
        page.get_by_role("link", name="Лицензии и документы").click()
        expect(page.locator("b-page")).to_contain_text("Лицензии и документы")

    with allure.step("2 - ERP users litsenziyasini ochish"):
        page.get_by_text("ERP users").first.click()
        page.get_by_role("button", name="Прикрепить пользователей").click()
        expect(page.get_by_role("heading")).to_contain_text("Прикрепленные пользователи")

    with allure.step("3 - Mavjud foydalanuvchilarni tozalab, yangi foydalanuvchini ulash"):
        try:
            no_data = page.locator('b-grid[name="table"]').get_by_text("нет данных")
            no_data.wait_for(state="visible", timeout=30_000)
        except PlaywrightTimeoutError:
            BasePage(page).checkbox(check_all=True, checked=True)
            page.get_by_role("button", name="Открепить").click()
            BasePage(page).confirm_biruni("Открепить пользователей в количестве")
            expect(page.locator("#kt_content")).to_contain_text("нет данных")

        page.get_by_role("button", name="Доступные").click()
        base_page = BasePage(page)
        base_page.wait_for_loader(timeout=120_000)
        page.get_by_role("searchbox", name="Поиск").fill(f"natural_person-pw{code}")
        page.get_by_role("searchbox", name="Поиск").press("Enter")
        base_page.wait_for_loader(timeout=120_000)

        page.get_by_text(f"natural_person-pw{code}").first.click()
        page.get_by_role("button", name="Прикрепить").click()
        expect(page.get_by_role("heading", name="Прикрепить пользователя")).to_be_visible()
        BasePage(page).confirm_biruni()
        page.get_by_role("button", name="Закрыть").click()

# ----------------------------------------------------------------------------------------------------------------------

@allure.title("Litsenziya sotib olish")
def test_buy_license(page, logger):
    run_buy_license(page, logger)


@allure.title("Foydalanuvchiga litsenziya ulash")
def test_attach_license(page, code, logger):
    run_attach_license(page, code, logger)
