import allure
from playwright.sync_api import Page, expect
from tests.smoke.flows.flow_authorization import authorization_user
from tests.smoke.flows.flow_navigate import navigate_to
from utils.base_page import BasePage

pytestmark = [allure.epic("Smoke"), allure.feature("Life Cycle"), allure.story("Init Balance")]

# ----------------------------------------------------------------------------------------------------------------------

def run_init_balance(page: Page, code, scope: str = "smoke") -> None:
    with allure.step("1 - Foydalanuvchi sifatida kirish va sahifani ochish"):
        authorization_user(page, code)
        navigate_to(page, tab="Склад", name="Ввод начальных остатков ТМЦ")
        expect(page.get_by_role("heading")).to_contain_text("Ввод начальных остатков ТМЦ")

    with allure.step("2 - Yangi hujjat yaratish va ma'lumot kiritish"):
        page.get_by_role("button", name="Создать").click()
        expect(page.get_by_role("heading")).to_contain_text("Ввод начальных остатков ТМЦ (создание)")
        page.get_by_role("textbox").first.fill(f"{code}")
        page.locator("b-pg-grid").get_by_role("textbox", name="Поиск").click()
        page.get_by_text(f"code_product-pw{code}").click()
        page.locator('input[ng-model="item.quantity"]').first.fill("100")
        page.locator('input[ng-model="item.price"]').first.fill("5000")

    with allure.step("3 - Saqlash va tasdiqlash"):
        page.get_by_role("button", name="Сохранить").click()
        BasePage(page).confirm_biruni("Сохранить?")
        expect(page.get_by_role("heading")).to_contain_text("Ввод начальных остатков ТМЦ")

    with allure.step("4 - Hujjatni o'tkazish (провести)"):
        page.get_by_text(f"{code}", exact=True).click()
        page.get_by_role("button", name="Провести").click()
        BasePage(page).confirm_biruni(f"Провести документ № {code}?")

    with allure.step("5 - Provodkalarni tekshirish (miqdor va summa)"):
        page.locator("#kt_content").get_by_text(f"{code}").click()
        with page.expect_popup() as page2_info:
            page.get_by_role("button", name="Проводки").click()
        page2 = page2_info.value
        expect(page2.get_by_role("rowgroup")).to_contain_text("100")
        expect(page2.get_by_role("rowgroup")).to_contain_text("500 000")

# ----------------------------------------------------------------------------------------------------------------------

@allure.title("Boshlang'ich qoldiqlarni kiritish va o'tkazish")
def test_init_balance(page: Page, code, test_scope) -> None:
    run_init_balance(page, code, scope=test_scope)
