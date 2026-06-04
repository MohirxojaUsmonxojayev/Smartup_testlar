import re

import allure
from playwright.sync_api import Page, expect

from tests.smoke.flows.flow_navigate import navigate_to
from utils.base_page import BasePage


def flow_create_initial_balance(
    page: Page,
    document_number: str,
    product_code: str,
    quantity="100",
    price="5000",
) -> None:
    with allure.step("Inventory: boshlang'ich qoldiq yaratish"):
        navigate_to(page, tab="Склад", name="Ввод начальных остатков ТМЦ")
        expect(page.get_by_role("heading")).to_contain_text("Ввод начальных остатков ТМЦ")
        page.get_by_role("button", name="Создать").click()
        expect(page.get_by_role("heading")).to_contain_text("Ввод начальных остатков ТМЦ (создание)")
        page.get_by_role("textbox").first.fill(document_number)
        page.locator("b-pg-grid").get_by_role("textbox", name="Поиск").click()
        page.get_by_text(product_code).click()
        page.locator('input[ng-model="item.quantity"]').first.fill(quantity)
        page.locator('input[ng-model="item.price"]').first.fill(price)

    with allure.step("Inventory: boshlang'ich qoldiqni saqlash"):
        page.get_by_role("button", name="Сохранить").click()
        BasePage(page).confirm_biruni("Сохранить?")
        expect(page.get_by_role("heading")).to_contain_text("Ввод начальных остатков ТМЦ")

    with allure.step("Inventory: boshlang'ich qoldiq hujjatini o'tkazish"):
        page.locator("#kt_content").get_by_text(document_number, exact=True).click()
        page.get_by_role("button", name="Провести").click()
        BasePage(page).confirm_biruni(f"Провести документ № {document_number}?")
        BasePage(page).wait_for_loader()
        expect(page).to_have_url(re.compile(r".*/init_inventory_balance_list"))
