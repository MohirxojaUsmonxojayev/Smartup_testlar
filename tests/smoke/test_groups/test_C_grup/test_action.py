import allure
from playwright.sync_api import Page, expect
from tests.smoke.flows.flow_authorization import authorization_user
from tests.smoke.flows.flow_navigate import navigate_to
from utils.base_page import BasePage

pytestmark = [allure.epic("C Group"), allure.feature("Marketing"), allure.story("Action")]


# ----------------------------------------------------------------------------------------------------------------------

def run_c_group_create_action(page: Page, code, scope: str = "smoke", login: bool = True) -> None:
    """C-01: 10 dona olinganda 10% chegirma beruvchi aksiya yaratish.

    Qadamlar:
      1. Справочники -> Маркетинг -> Акции ro'yxatiga o'tish
      2. Создать -> asosiy maydonlar: nom, рабочие зоны, бонусный склад (Тип акции = Кол-во)
      3. Далее -> Условие "Все ТМЦ" Мин. значение = 10
      4. Бонус: Тип бонуса = Скидка, product Значение(%) = 10
      5. Завершить -> "Сохранить?" tasdiqlash
      6. Ro'yxatda yaratilgan aksiya va "Активный" statusi tekshiriladi
    """
    action_name = f"Скидка 10% на 10 товаров pw{code}"

    if login:
        authorization_user(page, code)

    with allure.step("1 - Aksiyalar ro'yxatiga o'tish"):
        navigate_to(page, tab="Справочники", name="Акции")
        expect(page.get_by_role("heading", name="Акции")).to_be_visible()

    with allure.step("2 - Yangi aksiya formasi: asosiy maydonlar"):
        page.get_by_role("button", name="Создать").click()
        # Aksiya formasi wizard — bir nechta ko'rinadigan heading bor (Главное, Условия),
        # shuning uchun forma sarlavhasi aniq nom bilan nishonlanadi.
        expect(page.get_by_role("heading", name="Акция (создание)")).to_be_visible()

        page.locator("#anor718-input-text-name").get_by_role("textbox").fill(action_name)

        rooms = page.locator("#anor718-input-b_input-rooms")
        rooms.get_by_role("textbox", name="Поиск").click()
        page.get_by_text(f"room-pw{code}", exact=True).click()

        warehouse = page.locator("#anor718-input-b_input-bonus_warehouse")
        warehouse.get_by_role("textbox", name="Поиск").click()
        page.get_by_text("Основной склад", exact=True).click()

        # Тип акции = Кол-во (default qoldiriladi)
        page.get_by_role("button", name="Далее").click()
        expect(page.get_by_role("heading", name="Условия")).to_be_visible()

    with allure.step("3 - Условие: Все ТМЦ uchun Мин. значение = 10"):
        page.locator('input[ng-model="rule.main_value"]').fill("10")

    with allure.step("4 - Бонус: Скидка turi, productga 10% chegirma"):
        page.locator('[ng-model="bonus.bonus_kind"]').click()
        page.get_by_role("option", name="Скидка", exact=True).click()

        bonus_search = page.locator("#bonus_products").get_by_role("textbox", name="Поиск")
        bonus_search.click()
        bonus_search.fill(f"product-pw{code}")
        page.locator("#bonus_products").get_by_text(f"product-pw{code}", exact=True).first.click()

        page.locator('input[ng-model="product.value"]').fill("10")

    with allure.step("5 - Saqlash va ro'yxatda tekshirish"):
        BasePage(page).save_and_expect_heading(
            "Акции",
            action="Акция (создание) -> Завершить",
            before_state="Акция (создание)",
            expected_state="Акции list ochilishi",
            button_name="Завершить",
            confirm_text="Сохранить?",
            location_hint="tests/smoke/test_groups/test_C_grup/test_action.py::run_c_group_create_action",
        )
        page.get_by_role("searchbox", name="Поиск").fill(action_name)
        page.get_by_role("searchbox", name="Поиск").press("Enter")
        row = page.locator("b-grid .tbl-row").filter(has_text=action_name).first
        expect(row).to_be_visible()
        expect(row).to_contain_text("Активный")
