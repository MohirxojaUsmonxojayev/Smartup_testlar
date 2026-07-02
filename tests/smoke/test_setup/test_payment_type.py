import allure
from playwright.sync_api import expect
from tests.smoke.flows.flow_navigate import navigate_to, expect_page
from utils.base_page import BasePage

pytestmark = [allure.epic("Smoke"), allure.feature("Setup"), allure.story("Payment Type")]

# ----------------------------------------------------------------------------------------------------------------------

def run_payment_type(page):
    with allure.step("1 - To'lov turlari ro'yxatiga o'tish"):
        navigate_to(page, tab="Справочники", name="Цены")
        expect_page(page, heading="Цены")
        page.get_by_role("link", name="Типы оплат").click()
        expect_page(page, heading="Типы оплат")

    with allure.step("2 - Barcha to'lov turlarini tanlash va ulash"):
        page.get_by_role("button", name="Прикрепление").click()
        expect(page.get_by_role("heading")).to_contain_text("Тип оплат (прикрепление)")
        BasePage(page).checkbox(check_all=True, checked=True)
        page.get_by_role("button", name="Прикрепить").click()
        BasePage(page).confirm_biruni("Прикрепить типы оплат в количестве 4?")
        BasePage(page).wait_for_loader()
        expect(page.locator("b-grid")).to_contain_text("нет данных")
        page.get_by_role("button", name="Закрыть").click()

    with allure.step("3 - To'lov turlari ro'yxatida ko'rinishini tekshirish"):
        expect(page.locator("b-grid")).to_contain_text("Наличные деньги")
        expect(page.locator("b-grid")).to_contain_text("Перечисление")
        expect(page.locator("b-grid")).to_contain_text("Терминал")
        expect(page.locator("b-grid")).to_contain_text("Чековая книжка")

# ----------------------------------------------------------------------------------------------------------------------

@allure.title("To'lov turlarini tizimga ulash")
def test_payment_type(page):
    run_payment_type(page)
