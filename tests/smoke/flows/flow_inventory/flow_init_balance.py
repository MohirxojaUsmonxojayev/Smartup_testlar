import re

import allure
from playwright.sync_api import expect

from tests.smoke.flows.flow_navigate import navigate_to, expect_page
from utils.base_page import BasePage


def _select_main_warehouse(page):
    base_page = BasePage(page)
    base_page.select_b_input("d.warehouse_name", "Основной склад", clear=True)
    base_page.wait_for_loader()


def flow_create_initial_balance(
    page,
    document_number,
    product_code,
    quantity="100",
    price="5000",
):
    with allure.step("Inventory: boshlang'ich qoldiq yaratish"):
        navigate_to(page, tab="Склад", name="Ввод начальных остатков ТМЦ")
        expect_page(page, heading="Ввод начальных остатков ТМЦ")
        page.get_by_role("button", name="Создать").click()
        expect_page(page, heading="Ввод начальных остатков ТМЦ (создание)")
        page.get_by_role("textbox").first.fill(document_number)
        _select_main_warehouse(page)
        page.locator("b-pg-grid").get_by_role("textbox", name="Поиск").click()
        page.get_by_text(product_code).click()
        page.locator('input[ng-model="item.quantity"]').first.fill(quantity)
        page.locator('input[ng-model="item.price"]').first.fill(price)

    with allure.step("Inventory: boshlang'ich qoldiqni saqlash"):
        page.get_by_role("button", name="Сохранить", exact=True).first.click()
        BasePage(page).confirm_biruni("Сохранить?")
        BasePage(page).wait_for_loader()
        expect_page(page, heading="Ввод начальных остатков ТМЦ")
        expect(page).to_have_url(re.compile(r".*/init_inventory_balance_list"))

    with allure.step("Inventory: boshlang'ich qoldiq hujjatini o'tkazish"):
        BasePage(page).click_grid_row(document_number)
        page.get_by_role("button", name="Провести").click()
        BasePage(page).confirm_biruni(f"Провести документ № {document_number}?")
        BasePage(page).wait_for_loader()
        expect(page).to_have_url(re.compile(r".*/init_inventory_balance_list"))
