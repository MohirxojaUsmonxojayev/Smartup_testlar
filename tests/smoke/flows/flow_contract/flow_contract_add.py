import re

import allure
from playwright.sync_api import Page, expect

from utils.base_page import BasePage


def flow_contract_add_page(
    page: Page,
    code: str,
    contract_code: str,
    contract_name: str,
    amount="500000",
    payment_type=None,
) -> None:
    expect(page).to_have_url(re.compile(r".*/anor/mkf/contract\+add"))
    expect(page.locator("b-page")).to_contain_text("Номер*")
    expect(page.locator("b-page")).to_contain_text("Название*")
    expect(page.locator("b-page")).to_contain_text("Валюта*")

    with allure.step("Contract Add: asosiy majburiy maydonlarni to'ldirish"):
        BasePage(page).fill_textbox_by_label("Код", contract_code)
        BasePage(page).fill_textbox_by_label("Номер", code)
        BasePage(page).fill_textbox_by_label(
            "Название",
            contract_name,
            expected_value=re.compile(re.escape(contract_name)),
        )
        expect(page.get_by_text("Физическое лицо", exact=True)).to_be_visible()
        page.get_by_text("Физическое лицо", exact=True).click()
        BasePage(page).select_b_input_by_label("Физическое лицо", f"natural_client-pw{code}")
        BasePage(page).select_b_input_by_label("Валюта", "Узбекский сум")
        BasePage(page).fill_textbox_by_label("Сумма договора", amount)

    if payment_type:
        with allure.step(f"Contract Add: Типы оплат -> '{payment_type}' tanlash"):
            BasePage(page).select_b_input_by_label("Типы оплат", payment_type)


def flow_contract_save(page: Page) -> None:
    with allure.step("Contract Add: contractni saqlash"):
        page.get_by_role("button", name="Сохранить", exact=True).click()
        BasePage(page).wait_for_loader()
        expect(page).to_have_url(re.compile(r".*/anor/mkf/contract_list"))
        expect(page.get_by_role("heading")).to_contain_text("Договоры")


def flow_contract_assert_list_row(
    page: Page,
    code: str,
    contract_code: str,
    contract_name: str,
    amount_text="500 000",
) -> None:
    with allure.step("Contract List: yaratilgan contract qiymatlarini tekshirish"):
        expect(page.locator("b-grid")).to_contain_text(contract_code)
        expect(page.locator("b-grid")).to_contain_text(contract_name)
        expect(page.locator("b-grid")).to_contain_text(f"natural_client-pw{code}")
        expect(page.locator("b-grid")).to_contain_text("Узбекский сум")
        expect(page.locator("b-grid")).to_contain_text(amount_text)


def flow_contract_assert_view(
    page: Page,
    code: str,
    contract_code: str,
    contract_name: str,
    amount="500000",
    payment_type=None,
) -> None:
    with allure.step("Contract View: contract asosiy qiymatlarini tekshirish"):
        expect(page).to_have_url(re.compile(r".*/anor/mkf/contract_view"))
        expect(page.locator("b-page")).to_contain_text(contract_code)
        expect(page.locator("b-page")).to_contain_text(contract_name)
        expect(page.locator("b-page")).to_contain_text(f"natural_client-pw{code}")
        expect(page.locator("b-page")).to_contain_text("Узбекский сум")
        expect(page.locator("b-page")).to_contain_text(amount)
        if payment_type:
            expect(page.locator("b-page")).to_contain_text(payment_type)


def flow_contract_close_view(page: Page) -> None:
    with allure.step("Contract View: oynani yopish"):
        page.get_by_role("button", name="Закрыть", exact=True).click()
        expect(page).to_have_url(re.compile(r".*/anor/mkf/contract_list"))
        expect(page.get_by_role("heading")).to_contain_text("Договоры")
