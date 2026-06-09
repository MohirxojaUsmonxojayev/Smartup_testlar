import os
import re

import allure
import pytest
from playwright.sync_api import Page, expect
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from tests.smoke.flows.flow_authorization import login
from utils.base_page import BasePage

pytestmark = [allure.epic("Smoke"), allure.feature("Setup"), allure.story("Company")]

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
COMPANY_FORM_TIMEOUT = 60_000


def _env_flag(name: str) -> bool:
    return os.getenv(name, "").strip().lower() in {"1", "true", "yes", "on"}


def head_admin_email() -> str:
    value = os.getenv("HEAD_ADMIN_EMAIL", "").strip()
    if not value:
        raise AssertionError("--head-email majburiy: company yaratish uchun head profil emailini bering")
    return value


def head_admin_password() -> str:
    value = os.getenv("HEAD_ADMIN_PASSWORD", "").strip()
    if not value:
        raise AssertionError("--head-password majburiy: company yaratish uchun head profil parolini bering")
    return value


def company_code_for(code: str) -> str:
    return f"autotest{code}".lower()


def _company_code_text_pattern(company_code: str) -> re.Pattern:
    match = re.match(r"^([a-z]+)(\d+)$", company_code, re.IGNORECASE)
    if match:
        return re.compile(rf"{re.escape(match.group(1))}\s*{re.escape(match.group(2))}", re.IGNORECASE)
    return re.compile(re.escape(company_code), re.IGNORECASE)


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
    form = page.locator("#companyForm").first
    expect(form).to_be_visible(timeout=COMPANY_FORM_TIMEOUT)
    expect(form.locator("smt-control").first).to_be_visible(timeout=COMPANY_FORM_TIMEOUT)


def _labels_pattern(labels: tuple[str, ...]) -> re.Pattern:
    variants = "|".join(re.escape(label) for label in labels)
    return re.compile(rf"^\s*(?:{variants})\s*(?:\*)?\s*$", re.IGNORECASE)


def _find_control_by_labels(page: Page, labels: tuple[str, ...]):
    control = page.locator("smt-control").filter(
        has=page.locator("label").filter(has_text=_labels_pattern(labels))
    ).first
    try:
        expect(control).to_be_visible(timeout=COMPANY_FORM_TIMEOUT)
    except (AssertionError, PlaywrightTimeoutError):
        return None
    return control


def _control_by_label(page: Page, label: str):
    control = _find_control_by_labels(page, (label,))
    if control is None:
        raise AssertionError(f"Company formasida '{label}' control topilmadi")
    return control


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
    _select_data_option_by_label(page, "Маркировка", "UZ Marking")
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


def _open_company_security_tab(page: Page) -> None:
    for tab_name in ("Безопасность", "Security"):
        tab = page.get_by_text(tab_name, exact=True).first
        if tab.count() == 0:
            continue
        expect(tab).to_be_visible()
        tab.click()
        BasePage(page).wait_for_loader()
        expect(page.locator("body")).to_contain_text("Политика лицензирования")
        return
    raise AssertionError("Company viewda Security/Безопасность tab topilmadi")


def _setting_label(page: Page, labels: tuple[str, ...]):
    for label_text in labels:
        label = page.get_by_text(label_text, exact=True).first
        if label.count() > 0:
            expect(label).to_be_visible()
            return label
    raise AssertionError(f"Company Security tabida '{labels[0]}' label topilmadi")


def _setting_container(page: Page, labels: tuple[str, ...]):
    label = _setting_label(page, labels)

    for ancestor in (
        "ancestor::*[.//*[@role='switch'] or .//input[@type='checkbox'] or .//*[contains(@class,'switch')]][1]",
        "ancestor::smt-control[1]",
        "ancestor::*[contains(@class,'form-group')][1]",
        "ancestor::*[contains(@class,'col')][1]",
        "..",
    ):
        container = label.locator(f"xpath={ancestor}")
        if container.count() == 0:
            continue
        if (
            container.get_by_role("switch").count() > 0
            or container.locator("input[type='checkbox']").count() > 0
            or container.locator(".switch").count() > 0
            or container.get_by_role("radio").count() > 0
        ):
            return container.first

    raise AssertionError(f"'{labels[0]}' control topilmadi")


def _set_setting_enabled(page: Page, labels: tuple[str, ...], enabled: bool) -> bool:
    container = _setting_container(page, labels)

    switch = container.get_by_role("switch").first
    if switch.count() > 0 and switch.is_visible():
        current = switch.get_attribute("aria-checked")
        if current in {"true", "false"} and (current == "true") == enabled:
            return True
        try:
            switch.click(timeout=5_000)
        except PlaywrightTimeoutError:
            return False
        expect(switch).to_have_attribute("aria-checked", "true" if enabled else "false")
        return True

    checkbox = container.locator("input[type='checkbox']").first
    if checkbox.count() > 0:
        BasePage(page).set_checkbox(checkbox, checked=enabled)
        return True

    switch_fallback = container.locator(".switch").first
    if switch_fallback.count() > 0 and switch_fallback.is_visible():
        switch_text = re.sub(r"\s+", " ", switch_fallback.inner_text()).strip().lower()
        current = any(word in switch_text for word in ("да", "yes", "on", "вкл"))
        if current != enabled:
            switch_fallback.click()
        expected_text = re.compile(r"\b(да|yes|on|вкл)\b" if enabled else r"\b(нет|no|off|выкл)\b", re.IGNORECASE)
        expect(switch_fallback).to_contain_text(expected_text)
        return True

    if not enabled:
        off_option = container.get_by_text(re.compile(r"^\s*(нет|no|off|отключено|выкл)\s*$", re.IGNORECASE)).first
        if off_option.count() > 0 and off_option.is_visible():
            off_option.click()
            return True

    return False


def _set_license_policy_enabled(page: Page, enabled: bool) -> bool:
    return _set_setting_enabled(page, ("Политика лицензирования", "Licensing policy"), enabled)


def _disable_concurrent_session_limit(page: Page) -> bool:
    label = page.get_by_text("Ограничение количества одновременных сеансов", exact=True).first
    if label.count() == 0:
        return False
    expect(label).to_be_visible()

    container = label.locator(
        "xpath=ancestor::*[.//*[normalize-space()='Отключено'] and .//*[normalize-space()='1']][1]"
    ).first
    if container.count() == 0:
        return False

    disabled_option = container.get_by_role("button", name="Отключено", exact=True).first
    if disabled_option.count() == 0:
        disabled_option = container.get_by_text("Отключено", exact=True).first
    expect(disabled_option).to_be_visible()
    disabled_option.click()
    return True


def _save_company_changes(page: Page) -> None:
    save_button = page.get_by_role("button", name="Сохранить", exact=True).first
    expect(save_button).to_be_visible()
    save_button.click()
    confirm = page.locator("#biruniConfirm")
    try:
        expect(confirm).to_be_visible(timeout=3_000)
        expect(confirm).to_have_css("opacity", "1", timeout=3_000)
        confirm.get_by_role("button", name="да", exact=True).click()
        confirm.wait_for(state="hidden", timeout=30_000)
    except (AssertionError, PlaywrightTimeoutError):
        pass
    BasePage(page).wait_for_loader(timeout=600_000)


def _ensure_company_view(page: Page, company_code: str) -> None:
    try:
        _expect_page_title(page, re.compile(r"просмотр|View", re.IGNORECASE), timeout=5_000)
        return
    except (AssertionError, PlaywrightTimeoutError):
        pass

    close_button = page.get_by_role("button", name="Закрыть", exact=True).first
    if close_button.count() > 0 and close_button.is_visible():
        close_button.click()
        BasePage(page).wait_for_loader()

    _open_company_list(page)
    _assert_company_list_row(page, company_code)
    _open_company_view(page, company_code)


def _apply_company_security_settings(page: Page, company_code: str) -> None:
    _open_company_security_tab(page)

    if not _disable_concurrent_session_limit(page):
        raise AssertionError("'Ограничение количества одновременных сеансов' off qilinmadi")

    if _env_flag("DISABLE_LICENSE_POLICY") and not _set_license_policy_enabled(page, enabled=False):
        raise AssertionError("'Политика лицензирования' off qilinmadi")

    BasePage(page).wait_for_loader(timeout=600_000)

    save_button = page.get_by_role("button", name="Сохранить", exact=True).first
    if save_button.count() > 0 and save_button.is_visible():
        _save_company_changes(page)
        _ensure_company_view(page, company_code)


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
    company_code = company_code or company_code_for(code)

    with allure.step("1 - Head profilga kirish"):
        login(page, email=head_admin_email(), password=head_admin_password())
        expect(page.locator("a.menu-link.menu-toggle", has_text="Главное")).to_be_visible(timeout=120_000)

    with allure.step("2 - Company ro'yxatiga o'tish"):
        _open_company_list(page)

    with allure.step("3 - Company mavjud bo'lsa qayta yaratmasdan code saqlash"):
        if _company_exists(page, company_code):
            _open_company_view(page, company_code)
            _apply_company_security_settings(page, company_code)
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

    with allure.step("9 - Company viewda security sozlamalarini qo'llash"):
        _open_company_view(page, company_code)
        _apply_company_security_settings(page, company_code)

    with allure.step("10 - Company code ni data storega saqlash"):
        _save_company_code(save_data, company_code)

    return company_code


@allure.title("Company yaratish")
def test_company(page: Page, code, save_data, company_setup_enabled) -> None:
    """
    1. --head-email/--head-password bilan head profilga kirish.
    2. Главное -> Компании ro'yxatida yangi company yaratish.
    3. Код сервера, majburiy maydonlar va trade productlarini to'ldirib saqlash.
    4. Company ro'yxatida code bo'yicha tekshirish va data storega company_code saqlash.
    """
    if not company_setup_enabled:
        pytest.skip("Company setup faqat --create-company flagi bilan ishlaydi")
    run_company(page, code, save_data)
