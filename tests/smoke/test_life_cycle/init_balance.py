import allure
import re
from playwright.sync_api import expect
from tests.smoke.flows.flow_authorization import authorization
from tests.smoke.flows.flow_navigate import navigate_to, expect_page
from utils.base_page import BasePage

pytestmark = [allure.epic("Smoke"), allure.feature("Life Cycle"), allure.story("Init Balance")]

# ----------------------------------------------------------------------------------------------------------------------

def _select_main_warehouse(page):
    base_page = BasePage(page)
    base_page.select_b_input("d.warehouse_name", "Основной склад", clear=True)
    base_page.wait_for_loader()


def run_init_balance(page, code):
    with allure.step("1 - Foydalanuvchi sifatida kirish va sahifani ochish"):
        authorization(page, who="user", code=code)
        navigate_to(page, tab="Склад", name="Ввод начальных остатков ТМЦ")
        expect_page(page, heading="Ввод начальных остатков ТМЦ")

    with allure.step("2 - Yangi hujjat yaratish va ma'lumot kiritish"):
        page.get_by_role("button", name="Создать").click()
        expect(page.get_by_role("heading")).to_contain_text("Ввод начальных остатков ТМЦ (создание)")
        page.get_by_role("textbox").first.fill(f"{code}")
        _select_main_warehouse(page)
        page.locator("b-pg-grid").get_by_role("textbox", name="Поиск").click()
        page.get_by_text(f"code_product-pw{code}").click()
        page.locator('input[ng-model="item.quantity"]').first.fill("100")
        page.locator('input[ng-model="item.price"]').first.fill("5000")

    with allure.step("3 - Saqlash va tasdiqlash"):
        page.get_by_role("button", name="Сохранить", exact=True).first.click()
        BasePage(page).confirm_biruni("Сохранить?")
        BasePage(page).wait_for_loader()
        expect_page(page, heading="Ввод начальных остатков ТМЦ")
        expect(page).to_have_url(re.compile(r".*/init_inventory_balance_list"))

    with allure.step("4 - Hujjatni o'tkazish (провести)"):
        BasePage(page).click_grid_row(f"{code}")
        page.get_by_role("button", name="Провести").click()
        BasePage(page).confirm_biruni(f"Провести документ № {code}?")
        BasePage(page).wait_for_loader()
        expect(page).to_have_url(re.compile(r".*/init_inventory_balance_list"))

    with allure.step("5 - Provodkalarni tekshirish (miqdor va summa)"):
        BasePage(page).click_grid_row(f"{code}")
        with page.expect_popup() as page2_info:
            page.get_by_role("button", name="Проводки").click()
        page2 = page2_info.value
        expect(page2.get_by_role("rowgroup")).to_contain_text("100")
        expect(page2.get_by_role("rowgroup")).to_contain_text("500 000")

# ----------------------------------------------------------------------------------------------------------------------

@allure.title("Boshlang'ich qoldiqlarni kiritish va o'tkazish")
def test_init_balance(page, code):
    run_init_balance(page, code)
