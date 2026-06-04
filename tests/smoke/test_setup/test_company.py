import os
import re

import allure
import pytest
from playwright.sync_api import Page, expect
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from tests.smoke.flows.flow_authorization import COMPANY_URL, login
from utils.base_page import BasePage

pytestmark = [allure.epic("Smoke"), allure.feature("Setup"), allure.story("Company")]

HEAD_ADMIN_EMAIL = "admin@head"
HEAD_ADMIN_PASSWORD = "greenwhite"
PRODUCTION_COMPANY_URL = "https://smartup.online"
COMPANY_ACTIVATION_CODE = os.getenv("COMPANY_ACTIVATION_CODE", "").strip()
TRADE_CHILD_PRODUCTS = (
    "Call center",
    "Equipment",
    "Finance - Main",
    "Finance - Advanced",
    "HR and Payroll",
    "Image Recognition",
    "Main",
    "Manufacturing",
    "Marking",
    "Sales - Main",
    "Sales - Advanced",
    "Store",
    "Telegram",
    "Trade Marketing",
    "Uzbekistan Module",
    "Warehouse - Main",
    "Warehouse - Advanced",
)


def company_code_for(code: str) -> str:
    return f"autotest{code}".lower()


def _company_code_text_pattern(company_code: str) -> re.Pattern:
    match = re.match(r"^([a-z]+)(\d+)$", company_code, re.IGNORECASE)
    if match:
        return re.compile(rf"{re.escape(match.group(1))}\s*{re.escape(match.group(2))}", re.IGNORECASE)
    return re.compile(re.escape(company_code), re.IGNORECASE)


def _ensure_non_production_url() -> None:
    if COMPANY_URL.rstrip("/") == PRODUCTION_COMPANY_URL:
        raise AssertionError(
            "Company yaratish production serverda ishlamaydi. "
            "COMPANY_URL ni https://smartup.online dan boshqa test serverga o'zgartiring."
        )


def _expect_page_title(page: Page, title: re.Pattern | str, timeout: int | None = None) -> None:
    title_locator = page.locator("h1").first
    if timeout is None:
        expect(title_locator).to_be_visible()
        expect(title_locator).to_contain_text(title)
    else:
        expect(title_locator).to_be_visible(timeout=timeout)
        expect(title_locator).to_contain_text(title, timeout=timeout)


def _open_company_list(page: Page) -> None:
    page.locator("a.menu-link.menu-toggle", has_text="Главное").click()

    for name in ("Компании", "Company", "Companies"):
        link = page.locator("a.menu-link.menu-link-title").get_by_text(name, exact=True).first
        if link.count() > 0:
            link.click()
            BasePage(page).wait_for_loader()
            _expect_page_title(page, re.compile(r"Комп|Comp"))
            return

    raise AssertionError("Company menu topilmadi: Главное -> Компании")


def _company_exists(page: Page, company_code: str) -> bool:
    search = page.get_by_role("searchbox", name="Поиск")
    expect(search).to_be_visible()
    search.fill(company_code)
    search.press("Enter")
    BasePage(page).wait_for_loader()

    try:
        _wait_for_company_code_in_page(page, company_code, timeout=3_000)
        return True
    except (AssertionError, PlaywrightTimeoutError):
        return False


def _open_company_add(page: Page) -> None:
    page.get_by_role("button", name="Создать").click()
    BasePage(page).wait_for_loader()
    _expect_page_title(page, re.compile(r"создание|Creation", re.IGNORECASE))


def _label_pattern(label: str) -> re.Pattern:
    return re.compile(rf"^\s*{re.escape(label)}\s*(?:\*)?\s*$", re.IGNORECASE)


def _control_by_label(page: Page, label: str):
    control = page.locator("smt-control").filter(
        has=page.locator("label").filter(has_text=_label_pattern(label))
    ).first
    expect(control).to_be_visible()
    return control


def _find_control_by_labels(page: Page, labels: tuple[str, ...]):
    for label in labels:
        control = page.locator("smt-control").filter(
            has=page.locator("label").filter(has_text=_label_pattern(label))
        ).first
        if control.count() > 0:
            expect(control).to_be_visible()
            return control
    return None


def _fill_text_control_by_labels(page: Page, labels: tuple[str, ...], value: str) -> bool:
    control = _find_control_by_labels(page, labels)
    if control is None:
        return False

    textbox = control.get_by_role("textbox").first
    expect(textbox).to_be_visible()
    textbox.fill(value)
    expect(textbox).to_have_value(value)
    return True


def _fill_company_required_fields(page: Page, code: str, company_code: str) -> None:
    if not _fill_text_control_by_labels(page, ("Код сервера", "Server code"), company_code):
        raise AssertionError("Company add formasida 'Код сервера' maydoni topilmadi")

    if not _fill_text_control_by_labels(
        page,
        ("Название", "Наименование", "Company name", "Name"),
        f"Autotest company {code}",
    ):
        raise AssertionError("Company add formasida 'Название' maydoni topilmadi")

    language = _control_by_label(page, "Язык").get_by_role("textbox").first
    expect(language).to_have_value(re.compile(r"Русский|Russian", re.IGNORECASE))


def _open_data_select_by_label(page: Page, label: str) -> None:
    control = _control_by_label(page, label)
    trigger = control.locator("smt-select-trigger").first
    if trigger.count() > 0:
        expect(trigger).to_be_visible()
        trigger.click()
        return

    textbox = control.get_by_role("textbox").first
    expect(textbox).to_be_visible()
    textbox.click()


def _select_data_option_by_label(page: Page, label: str, option_text: str) -> None:
    _open_data_select_by_label(page, label)

    overlay = page.locator(".cdk-overlay-container")
    expect(overlay).to_contain_text(option_text)
    option = overlay.locator("li, [role='option']").filter(has_text=option_text).first
    if option.count() == 0:
        option = overlay.get_by_text(option_text, exact=True).first
    expect(option).to_be_visible()
    option.click()
    expect(_control_by_label(page, label).get_by_role("textbox").first).to_have_value(
        re.compile(re.escape(option_text))
    )
    BasePage(page).wait_for_loader()


def _select_required_templates(page: Page) -> None:
    _select_data_option_by_label(page, "План счетов", "UZ COA")
    _select_data_option_by_label(page, "Банки", "UZ BANK")


def _products_card(page: Page):
    title = page.get_by_role("heading", name=re.compile(r"^products$", re.IGNORECASE)).first
    expect(title).to_be_visible()
    card = title.locator("xpath=ancestor::section[contains(@class, 'custom-card')][1]")
    expect(card).to_be_visible()
    return card


def _product_switch(page: Page, product_name: str):
    label = _products_card(page).get_by_text(
        re.compile(rf"^\s*{re.escape(product_name)}\s*$", re.IGNORECASE)
    ).first
    expect(label).to_be_visible()
    switch = label.locator("xpath=ancestor::*[.//*[@role='switch']][1]").get_by_role("switch").first
    expect(switch).to_be_visible()
    return switch


def _set_product_switch(page: Page, product_name: str, checked: bool = True) -> None:
    switch = _product_switch(page, product_name)
    if (switch.get_attribute("aria-checked") == "true") != checked:
        switch.click()
    expect(switch).to_have_attribute("aria-checked", "true" if checked else "false")


def _click_trade_product(page: Page) -> None:
    _set_product_switch(page, "trade", checked=True)
    BasePage(page).wait_for_loader()
    expect(_products_card(page)).to_contain_text("Warehouse - Advanced", timeout=30_000)


def _click_trade_child_products(page: Page) -> None:
    clicked = []
    skipped = []
    for product_name in TRADE_CHILD_PRODUCTS:
        switch = _product_switch(page, product_name)
        if switch.get_attribute("aria-checked") != "true":
            switch.click()
            expect(switch).to_have_attribute("aria-checked", "true")
            clicked.append(product_name)
        else:
            skipped.append(product_name)

    result = {"clicked": clicked, "skipped": skipped, "childCount": len(clicked) + len(skipped)}
    allure.attach(str(result), name="company-product-controls", attachment_type=allure.attachment_type.TEXT)
    if result["childCount"] != len(TRADE_CHILD_PRODUCTS):
        raise AssertionError("Trade child productlar to'liq yoqilmadi")
    BasePage(page).wait_for_loader()


def _save_company_form(page: Page) -> None:
    page.get_by_role("button", name="Сохранить").click()
    confirm_candidates = (
        page.locator("#biruniConfirm"),
        page.get_by_role("dialog").filter(has=page.get_by_role("button", name="да", exact=True)),
    )
    for confirm in confirm_candidates:
        try:
            expect(confirm).to_be_visible(timeout=3_000)
        except (AssertionError, PlaywrightTimeoutError):
            continue
        try:
            expect(confirm).to_have_css("opacity", "1", timeout=3_000)
        except (AssertionError, PlaywrightTimeoutError):
            pass
        confirm.get_by_role("button", name="да", exact=True).first.click()
        confirm.wait_for(state="hidden", timeout=30_000)
        break
    BasePage(page).wait_for_loader(timeout=600_000)
    _expect_page_title(page, re.compile(r"^\s*(Компании|Companies)\s*$", re.IGNORECASE), timeout=600_000)


def _click_visible_button_by_text(page: Page, text: str) -> bool:
    buttons = page.get_by_role("button")
    for index in range(buttons.count()):
        button = buttons.nth(index)
        if not button.is_visible():
            continue
        button_text = re.sub(r"\s+", " ", button.inner_text()).strip()
        if text.lower() in button_text.lower():
            button.click()
            return True
    return False


def _assert_company_list_row(page: Page, company_code: str) -> None:
    search = page.get_by_role("searchbox", name="Поиск")
    expect(search).to_be_visible()
    search.fill(company_code)
    search.press("Enter")
    BasePage(page).wait_for_loader()
    _wait_for_company_code_in_page(page, company_code, timeout=10_000)


def _open_company_view(page: Page, company_code: str) -> None:
    page.get_by_text(_company_code_text_pattern(company_code)).first.click()
    if not _click_visible_button_by_text(page, "Просмотреть"):
        raise AssertionError("Company listda 'Просмотреть' button topilmadi")
    BasePage(page).wait_for_loader()
    _expect_page_title(page, re.compile(r"просмотр|View", re.IGNORECASE))


def _activate_company_for_license_if_configured(page: Page) -> None:
    activation_tab = page.get_by_text("Активация для лицензии", exact=True).first
    expect(activation_tab).to_be_visible()
    activation_tab.click()
    BasePage(page).wait_for_loader()
    expect(page.locator("body")).to_contain_text("Код активации")

    if page.locator("body").get_by_text("Активирован", exact=True).count() > 0:
        return

    if not COMPANY_ACTIVATION_CODE:
        allure.attach(
            "COMPANY_ACTIVATION_CODE berilmagan. License sotib olish uchun yangi company "
            "viewidagi 'Активация для лицензии' tabida activation code kiritilishi kerak.",
            name="company-license-activation-missing",
            attachment_type=allure.attachment_type.TEXT,
        )
        return

    textbox = page.get_by_role("textbox").first
    expect(textbox).to_be_visible()
    textbox.fill(COMPANY_ACTIVATION_CODE)
    activate = page.get_by_role("button", name="Активация", exact=True)
    expect(activate).to_be_enabled()
    activate.click()
    BasePage(page).wait_for_loader(timeout=600_000)
    expect(page.locator("body")).to_contain_text("Активирован")


def _wait_for_company_code_in_page(page: Page, company_code: str, timeout: int) -> None:
    try:
        expect(page.locator("body")).to_contain_text(_company_code_text_pattern(company_code), timeout=timeout)
    except (AssertionError, PlaywrightTimeoutError) as exc:
        body_text = page.locator("body").inner_text()
        allure.attach(body_text, name="company-list-body-text", attachment_type=allure.attachment_type.TEXT)
        raise AssertionError(f"Company listda '{company_code}' topilmadi") from exc


def _save_company_code(save_data, company_code: str) -> None:
    if save_data is not None:
        save_data("company_code", company_code)


def run_company(page: Page, code, save_data=None, company_code: str | None = None) -> str:
    _ensure_non_production_url()
    company_code = company_code or company_code_for(code)

    with allure.step("1 - Head profilga kirish"):
        login(page, email=HEAD_ADMIN_EMAIL, password=HEAD_ADMIN_PASSWORD)
        expect(page.locator("a.menu-link.menu-toggle", has_text="Главное")).to_be_visible(timeout=120_000)

    with allure.step("2 - Company ro'yxatiga o'tish"):
        _open_company_list(page)

    with allure.step("3 - Company mavjud bo'lsa qayta yaratmasdan code saqlash"):
        if _company_exists(page, company_code):
            _open_company_view(page, company_code)
            _activate_company_for_license_if_configured(page)
            _save_company_code(save_data, company_code)
            return company_code

    with allure.step("4 - Yangi company formasida majburiy maydonlarni to'ldirish"):
        _open_company_add(page)
        _fill_company_required_fields(page, code, company_code)

    with allure.step("5 - Majburiy shablonlarni tanlash"):
        _select_required_templates(page)

    with allure.step("6 - Products card ichida trade va child productlarni yoqish"):
        _click_trade_product(page)
        _click_trade_child_products(page)

    with allure.step("7 - Company saqlash"):
        _save_company_form(page)

    with allure.step("8 - Ro'yxatda yaratilgan company code ni tekshirish"):
        _assert_company_list_row(page, company_code)

    with allure.step("9 - License uchun company activation holatini tekshirish"):
        _open_company_view(page, company_code)
        _activate_company_for_license_if_configured(page)

    with allure.step("10 - Company code ni data storega saqlash"):
        _save_company_code(save_data, company_code)

    return company_code


@allure.title("Company yaratish")
def test_company(page: Page, code, save_data, company_setup_enabled) -> None:
    """
    1. admin@head bilan head profilga kirish.
    2. Главное -> Компании ro'yxatida yangi company yaratish.
    3. Код сервера, majburiy maydonlar va trade productlarini to'ldirib saqlash.
    4. Company ro'yxatida code bo'yicha tekshirish va data storega company_code saqlash.
    """
    if not company_setup_enabled:
        pytest.skip("Company setup faqat production bo'lmagan COMPANY_URL bilan ishlaydi")
    run_company(page, code, save_data)
