import allure
from playwright.sync_api import Page, expect
from tests.smoke.flows.flow_navigate import navigate_to

pytestmark = [allure.epic("Smoke"), allure.feature("Life Cycle"), allure.story("Balance")]

# ----------------------------------------------------------------------------------------------------------------------

def run_balance(page: Page, code, scope: str = "smoke") -> None:
    with allure.step("1 - TMC qoldiqlar sahifasiga o'tish"):
        navigate_to(page, tab="Склад", name="Остатки ТМЦ")
        expect(page.get_by_role("heading")).to_contain_text("Остатки ТМЦ")

    with allure.step("2 - Mahsulot qoldig'i ro'yxatda ko'rinishini tekshirish"):
        expect(page.locator("b-page")).to_contain_text(f"code_product-pw{code}")

# ----------------------------------------------------------------------------------------------------------------------

@allure.title("TMC qoldiqlarini tekshirish")
def test_balance(page: Page, code, test_scope) -> None:
    run_balance(page, code, scope=test_scope)
