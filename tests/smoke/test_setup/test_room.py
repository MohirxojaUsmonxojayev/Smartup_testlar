import allure
from playwright.sync_api import Page, expect
from tests.smoke.flows.flow_authorization import authorization, USER_PASS, user_email_for
from tests.smoke.flows.flow_navigate import navigate_to, switch_filial
from utils.base_page import BasePage

pytestmark = [allure.epic("Smoke"), allure.feature("Setup"), allure.story("Room")]

# ----------------------------------------------------------------------------------------------------------------------

def _select_grid_checkall(page: Page, grid_name: str) -> None:
    grid = page.locator(f'b-grid[name="{grid_name}"]')
    expect(grid).to_be_visible()
    checkbox = grid.locator("input[bcheckall]").first
    if checkbox.count() == 0:
        checkbox = grid.locator('input[type="checkbox"]').first
    BasePage(page).set_checkbox(checkbox, checked=True)

# ----------------------------------------------------------------------------------------------------------------------

def run_room(page: Page, code, scope: str = "smoke") -> None:
    with allure.step("1 - Ish zonalari ro'yxatiga o'tish"):
        switch_filial(page, name=f"filial-pw{code}")
        navigate_to(page, tab="Справочники", name="Рабочие зоны")
        expect(page.get_by_role("heading")).to_contain_text("Рабочие зоны")

    with allure.step("2 - Yangi ish zonasi formasini to'ldirish"):
        page.get_by_role("button", name="Создать").click()
        expect(page.get_by_role("heading")).to_contain_text("Рабочая зона (создание)")
        page.get_by_role("textbox").first.fill(f"code_room_pw{code}")
        page.get_by_role("textbox").nth(1).fill(f"room-pw{code}")
        expect(page.get_by_text("Активный").first).to_be_visible()

    with allure.step("3 - Saqlash va ro'yxatda tekshirish"):
        BasePage(page).save_and_expect_heading(
            "Рабочие зоны",
            action="Рабочая зона (создание) -> Сохранить",
            before_state="Рабочая зона (создание)",
            expected_state="Рабочие зоны list ochilishi",
            location_hint="tests/smoke/test_setup/test_room.py::run_room",
        )
        expect(page.get_by_text(f"room-pw{code}")).to_be_visible()
        expect(page.get_by_text(f"code_room_pw{code}")).to_be_visible()

# ----------------------------------------------------------------------------------------------------------------------

def run_room_attachment(page: Page, code, scope: str = "smoke") -> None:
    with allure.step("1 - Foydalanuvchi sifatida kirish va ish zonasini ochish"):
        authorization(page, email=user_email_for(code), password=USER_PASS)
        navigate_to(page, tab="Справочники", name="Рабочие зоны")
        expect(page.get_by_role("heading")).to_contain_text("Рабочие зоны")
        page.get_by_text(f"room-pw{code}").click()
        page.get_by_role("button", name="Прикрепление").click()
        expect(page.locator("#kt_content")).to_contain_text(f"Рабочая зона (прикрепление): room-pw{code}")

    with allure.step("2 - To'lov turlarini ulash"):
        page.get_by_role("link", name="Типы оплат").click()
        expect(page.locator("b-page")).to_contain_text("Типы оплат")
        page.get_by_role("button", name="Доступные").click()
        BasePage(page).wait_for_loader()
        _select_grid_checkall(page, "table_payment_type")
        page.get_by_role("button", name="Прикрепить").click()
        BasePage(page).confirm_biruni("Прикрепить 4?")
        expect(page.locator("b-page")).to_contain_text("нет данных")

    with allure.step("3 - Skladni ulash"):
        page.get_by_role("link", name="Склады").click()
        expect(page.locator("b-page")).to_contain_text("Склады")
        page.get_by_role("button", name="Доступные").click()
        BasePage(page).wait_for_loader()
        _select_grid_checkall(page, "table_warehouse")
        page.get_by_role("button", name="Прикрепить").click()
        BasePage(page).confirm_biruni("Прикрепить 1?")
        expect(page.locator("b-page")).to_contain_text("нет данных")

    with allure.step("4 - Kassani ulash"):
        page.get_by_role("link", name="Кассы").click()
        expect(page.locator("b-page")).to_contain_text("Кассы")
        page.get_by_role("button", name="Доступные").click()
        BasePage(page).wait_for_loader()
        _select_grid_checkall(page, "table_cashbox")
        page.get_by_role("button", name="Прикрепить").click()
        BasePage(page).confirm_biruni("Прикрепить 1?")
        expect(page.locator("b-page")).to_contain_text("нет данных")

    with allure.step("5 - Mijozni ulash"):
        page.get_by_role("link", name="Физические лица").click()
        expect(page.locator("b-page")).to_contain_text("Физические лица")
        page.get_by_role("button", name="Доступные").click()
        page.get_by_text(f"natural_client-pw{code}").click()
        page.get_by_role("button", name="Прикрепить").click()
        BasePage(page).confirm_biruni(f"Прикрепить natural_client-pw{code}?")
        page.get_by_role("button", name="Прикрепленные").click()
        expect(page.locator("b-page")).to_contain_text(f"natural_client-pw{code}")

    with allure.step("6 - Sahifani yopish"):
        page.get_by_role("button", name="Закрыть").click()
        expect(page.get_by_role("heading")).to_contain_text("Рабочие зоны")

# ----------------------------------------------------------------------------------------------------------------------

@allure.title("Ish zonasi yaratish")
def test_room(page: Page, code, test_scope) -> None:
    run_room(page, code, scope=test_scope)


@allure.title("Ish zonasiga to'lov, sklad, kassa va mijoz ulash")
def test_room_attachment(page: Page, code, test_scope) -> None:
    run_room_attachment(page, code, scope=test_scope)
