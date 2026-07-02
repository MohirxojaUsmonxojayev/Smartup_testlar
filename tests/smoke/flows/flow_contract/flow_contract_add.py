import re

import allure
from playwright.sync_api import expect
from tests.smoke.flows.flow_navigate import expect_page

from utils.base_page import BasePage


def flow_contract_add_page(
    page,
    code,
    contract_code,
    contract_name,
    amount="500000",
    payment_type=None,
):
    expect(page).to_have_url(re.compile(r".*/anor/mkf/contract\+add"))
    BasePage(page).wait_for_loader()
    expect(page.locator("b-page")).to_contain_text("Номер*")
    expect(page.locator("b-page")).to_contain_text("Название*")
    expect(page.locator("b-page")).to_contain_text("Валюта*")

    with allure.step("Contract Add: asosiy majburiy maydonlarni to'ldirish"):
        base = BasePage(page)
        base.input(label="Код", value=contract_code)
        base.input(label="Номер", value=code)
        base.input(
            label="Название",
            value=contract_name,
            expect_value=re.compile(re.escape(contract_name)),
        )
        expect(page.get_by_text("Физическое лицо", exact=True)).to_be_visible()
        page.get_by_text("Физическое лицо", exact=True).click()
        base.b_input_by_label("Физическое лицо", value=f"natural_client-pw{code}")
        base.b_input_by_label("Валюта", value="Узбекский сум")
        base.input(label="Сумма договора", value=amount)

    if payment_type:
        with allure.step(f"Contract Add: Типы оплат -> '{payment_type}' tanlash"):
            BasePage(page).b_input_by_label("Типы оплат", value=payment_type)


def flow_contract_save(page):
    with allure.step("Contract Add: contractni saqlash"):
        page.get_by_role("button", name="Сохранить", exact=True).first.click()
        BasePage(page).wait_for_loader()
        expect_page(page, heading="Договоры")
        expect(page).to_have_url(re.compile(r".*/anor/mkf/contract_list"))


def flow_contract_assert_list_row(
    page,
    code,
    contract_code,
    contract_name,
    amount_text="500 000",
):
    with allure.step("Contract List: yaratilgan contract qiymatlarini tekshirish"):
        expect(page.locator("b-grid")).to_contain_text(contract_code)
        expect(page.locator("b-grid")).to_contain_text(contract_name)
        expect(page.locator("b-grid")).to_contain_text(f"natural_client-pw{code}")
        expect(page.locator("b-grid")).to_contain_text("Узбекский сум")
        expect(page.locator("b-grid")).to_contain_text(amount_text)


def flow_contract_assert_view(
    page,
    code,
    contract_code,
    contract_name,
    amount="500000",
    payment_type=None,
):
    with allure.step("Contract View: contract asosiy qiymatlarini tekshirish"):
        expect(page).to_have_url(re.compile(r".*/anor/mkf/contract_view"))
        expect(page.locator("b-page")).to_contain_text(contract_code)
        expect(page.locator("b-page")).to_contain_text(contract_name)
        expect(page.locator("b-page")).to_contain_text(f"natural_client-pw{code}")
        expect(page.locator("b-page")).to_contain_text("Узбекский сум")
        expect(page.locator("b-page")).to_contain_text(amount)
        if payment_type:
            expect(page.locator("b-page")).to_contain_text(payment_type)


def flow_contract_close_view(page):
    with allure.step("Contract View: oynani yopish"):
        page.get_by_role("button", name="Закрыть", exact=True).click()
        expect(page).to_have_url(re.compile(r".*/anor/mkf/contract_list"))
        expect(page.get_by_role("heading")).to_contain_text("Договоры")
